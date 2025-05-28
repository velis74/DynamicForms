import re

from enum import auto
from typing import Any, Dict

from django.template import loader
from rest_framework.reverse import reverse
from rest_framework.serializers import Serializer, SerializerMetaclass

from dynamicforms import fields
from dynamicforms.action import TableAction, TablePosition
from dynamicforms.mixins import ActionMixin, DisplayMode, FieldRenderMixin

from .base import ViewModeBase
from .render_mode_enum import ViewModeEnum
from .serializer_filter import SerializerFilter
from .serializer_render_actions import SerializerRenderActions
from .serializer_render_fields import SerializerRenderFields
from .util import convert_to_json_if

# noinspection PyUnreachableCode
if False:
    from .listserializer import ViewModeListSerializer


class ViewModeSerializer(ViewModeBase, SerializerFilter, metaclass=SerializerMetaclass):
    """
    This one is actually a mixin, not a monkey-patch like the other two
    """

    bound_value = None

    class ViewMode(ViewModeEnum):
        FORM = auto()  # Render to form field
        TABLE_ROW = auto()  # Render to table tr
        TABLE_HEAD = auto()  # Render to table header

    df_control_data = fields.SerializerMethodField(display=DisplayMode.HIDDEN, read_only=True)
    show_filter = True

    @property
    def component_name(self):
        """
        component_name returns name of Vue component to use for rendering this serializer's form
        by default it will take the HTML template's form_template parameter and replace all non-compliant
        characters with '-'.

        Usually, though, you will replace this property with one of your own declaring your Vue component name to
        instantiate. The component is expected to behave like DFFormLayout does
        :return: name of component to use when rendering the layout in VDOM
        """
        res = getattr(self, "form_template", "df-form-layout")
        res = re.sub(r"[^a-zA-Z0-9._-]", "-", res)
        return res

    """
    we're currently using two additional headers for axios:
    'x-viewmode': 'TABLE_ROW' - tells DF what viewMode to use for rendering the response
    'x-pagination': 1 - tells DRF to paginate (or not) the result
    """

    def __init__(
        self,
        *args,
        view_mode: "ViewModeSerializer.ViewMode" = None,
        view_mode_list: "ViewModeListSerializer.ViewMode" = None,
        **kwds,
    ):
        super().__init__(*args, **kwds)
        if not view_mode and self.request and "HTTP_X_VIEWMODE" in self.request.META:
            view_mode = self.ViewMode[self.request.META["HTTP_X_VIEWMODE"]]
        self.set_view_mode(view_mode)
        self.view_mode_list = view_mode_list

    def __new__(cls, *args, **kwargs):
        from .listserializer import ViewModeListSerializer

        view_mode_list = kwargs.pop("view_mode_list", None)

        # Set list_serializer_class of class Meta
        meta = getattr(cls, "Meta", None)
        if meta is None:
            meta = type("Meta", (object,), {})
            cls.Meta = meta
        if not hasattr(meta, "list_serializer_class"):
            meta.list_serializer_class = ViewModeListSerializer

        res = super().__new__(cls, *args, **kwargs)
        if isinstance(res, ViewModeListSerializer):
            if not view_mode_list and res.child.view_mode == ViewModeSerializer.ViewMode.TABLE_ROW:
                view_mode_list = ViewModeListSerializer.ViewMode.TABLE

            res.set_view_mode(view_mode_list)
            res.display_table = res.child.display_table
            res.display_form = res.child.display_form

        return res

    def set_bound_value(self, value: Dict[Any, Any]):
        self.bound_value = value

    @property
    def request(self: "_ViewModeBoundSerializer"):
        if self.context and "view" in self.context and self.context["view"].request:
            return self.context["view"].request
        return None

    def render_form(self: "_ViewModeBoundSerializer"):
        template = loader.get_template("template_render/full_form.html")
        context = dict(serializer=self, columns=self.render_fields)
        return template.render(context)

    @property
    def render_fields(self: "_ViewModeBoundSerializer"):
        this = self

        class BoundSerializerRenderFields(SerializerRenderFields):
            @property
            def fields(self):
                actions = [a for a in this.actions.renderable_actions(this) if isinstance(a, TableAction)]
                if any(getattr(action, "position", None) == TablePosition.ROW_START for action in actions):
                    yield SerializerRenderFields.ActionField(actions, TablePosition.ROW_START)

                for f in this.fields.values():
                    if f.display_table != DisplayMode.SUPPRESS:
                        yield f

                if any(getattr(action, "position", None) == TablePosition.ROW_END for action in actions):
                    yield SerializerRenderFields.ActionField(actions, TablePosition.ROW_END)

        return BoundSerializerRenderFields()

    @property
    def render_actions(self: "_ViewModeBoundSerializer"):
        this = self

        class BoundSerializerRenderActions(SerializerRenderActions):
            @property
            def actions(self):
                return this.actions.renderable_actions(this)

        return BoundSerializerRenderActions()

    # noinspection PyMethodMayBeStatic
    def get_default_data(self):
        # This is useful if we have subserializer on form... When user clicks add record form uses this data.
        # Use example:
        #
        #   default = self.get_initial()
        #   if isinstance(default, dict):
        #       default["my_field"] = "Default data"
        #   return default
        return None

    def component_params(self: "_ViewModeBoundSerializer", output_json: bool = True):
        from dynamicforms.utils import get_pk_name

        if getattr(self, "Meta", None) and getattr(self.Meta, "model", None):
            primary_key_name = get_pk_name(self.Meta.model)
        else:
            primary_key_name = "id"

        params = {
            "uuid": self.uuid,
            "primary_key_name": primary_key_name,
            "titles": self.form_titles,
            "columns": [c.as_component_def() for c in self.render_fields.fields],
            "responsive_table_layouts": self.get_responsive_table_layouts_def(),
            "actions": self.render_actions.as_action_def(),
            "record": self.get_default_data() if self.parent else self.data,
            "filter": self.filter_serializer_component_params() if self.show_filter else None,
            "row_select": bool(getattr(self, "row_select", False)),
            "dialog": self.get_dialog_def(),
            "detail_url": self.reverse_url if not self.is_filter else None,
            "ordering_parameter": getattr(self.context["view"], "ordering_parameter", "ordering"),
            "ordering_style": getattr(self.context["view"], "ordering_style", None),
        }
        return convert_to_json_if(params, output_json)

    def get_df_control_data(self: "_ViewModeBoundSerializer", row):
        """
        Returns any additional data needed for rendering or operating the serializer on the client, such as presence of
        action buttons, their parameters, CSS, etc.

          deprecates row_css_style and df_prev_link

        :param row: row data to consider when presenting the return data
        :return: dict of settings for actions and row-related data
        """
        return dict(
            row_css_style=self.get_row_css_style(row),
            actions=dict(
                filter(
                    lambda x: x[1] is not None,
                    (action.to_component_params(row, self) for action in self.render_actions.actions),
                )
            ),
        )

    @property
    def layout(self):
        template_context = getattr(self, "template_context", {})
        if hasattr(self, "determine_layout_at_runtime") and (layout := self.determine_layout_at_runtime(self.request)):
            return layout
        elif hasattr(self, "Meta") and hasattr(self.Meta, "layout"):
            return self.Meta.layout
        else:
            from dynamicforms.template_render.layout import Layout

            return Layout(
                size=template_context.get("dialog_classes", ""),
                header_classes=template_context.get("dialog_header_classes", ""),
            )

    def get_dialog_def(self):
        return self.layout.as_component_def(self)

    @property
    def responsive_table_layouts(self):
        if hasattr(self, "Meta") and hasattr(self.Meta, "responsive_columns"):
            return self.Meta.responsive_columns
        return None

    def get_responsive_table_layouts_def(self):
        return self.responsive_table_layouts and self.responsive_table_layouts.as_component_def(self)

    @classmethod
    def get_reverse_url(cls, view_name, request, kwargs=None):
        return reverse(view_name + "-detail", format="json", request=request, kwargs=kwargs)

    @classmethod
    def get_component_context(cls, request, queryset):
        from rest_framework.request import Request

        from dynamicforms.filters import FilterBackend
        from dynamicforms.template_render import ViewModeListSerializer, ViewModeSerializer
        from dynamicforms.viewsets import ModelViewSet

        class FakeViewSet(object):
            """
            We fake a DRF ViewSet here to get ordering and pagination to work
            """

            def __init__(self, request, queryset):
                self.filter_backend = FilterBackend()
                self.request = request
                self.queryset = queryset

            @property
            def ordering(self):
                return self.filter_backend.get_ordering(self.request, self.queryset, None)

        paginator = ModelViewSet.generate_paged_loader()()

        # first we try to paginate the queryset, together with some sort ordering & stuff
        req = Request(request)
        req.accepted_renderer = None  # viewsets.py->MyCursorPagination.encode_cursor
        viewset = FakeViewSet(req, queryset)
        page = paginator.paginate_queryset(queryset, req)
        if page is None:
            # if unsuccessful, just resume with the entire queryset
            page = queryset

        ser = cls(
            page,
            view_mode=ViewModeSerializer.ViewMode.TABLE_ROW,
            view_mode_list=ViewModeListSerializer.ViewMode.TABLE,
            context=dict(view=viewset),
            many=True,
        )
        base_url = paginator.base_url.split("?", 1)
        ser.reverse_url = ser.get_reverse_url(cls.template_context["url_reverse"], request)
        ser.child.reverse_url = ser.child.get_reverse_url(
            cls.template_context["url_reverse"], request, kwargs=dict(pk="--record_id--")
        )
        paginator.base_url = ser.reverse_url + (("?" + base_url[1]) if len(base_url) == 2 else "")
        ser.paginator = paginator
        return ser

    @property
    def default_url_reverse_kwargs(self):
        if not self.parent and "id" not in self.data:
            return dict(pk=None)
        else:
            return dict(pk=self.data["id"] if not getattr(self, "parent", None) else "--record_id--")

    def apply_component_context(self, request=None, paginator=None):
        # Different to ViewModeSerializer.get_component_context - which is a class method creating the instances
        # this one will decorate existing instance with the appropriate values needed for rendering
        # in all other respects, they are the same

        request = request or self.request
        paginator = paginator or self.context.get("view", type("NoView", (object,), dict(paginator=None))).paginator

        if not self.view_mode:
            self.view_mode = (
                ViewModeSerializer.ViewMode.TABLE_ROW
                if self.master and isinstance(self.master, ViewModeListSerializer)
                else ViewModeSerializer.ViewMode.FORM
            )

        self.reverse_url = self.get_reverse_url(
            self.template_context["url_reverse"],
            request,
            self.template_context.get("url_reverse_kwargs", self.default_url_reverse_kwargs),
        )


# noinspection PyAbstractClass
class _ViewModeBoundSerializer(ViewModeSerializer, FieldRenderMixin, ActionMixin, Serializer):
    """
    Dummy class just for type hinting
    """

    class FakeActionsList(list):
        def renderable_actions(self, _unused):
            return self

    actions = FakeActionsList()
