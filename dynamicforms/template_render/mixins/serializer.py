from enum import auto
from typing import Any, Dict

from rest_framework.reverse import reverse
from rest_framework.serializers import ListSerializer, Serializer, SerializerMetaclass

from dynamicforms import fields
from dynamicforms.action import TablePosition
from dynamicforms.mixins import ActionMixin, DisplayMode, RenderMixin
from .base import ViewModeBase
from .render_mode_enum import ViewModeEnum
from .serializer_render_actions import SerializerRenderActions
from .serializer_render_fields import SerializerRenderFields
from .util import convert_to_json_if

# noinspection PyUnreachableCode
if False:
    from .listserializer import ViewModeListSerializer


class ViewModeSerializer(ViewModeBase, metaclass=SerializerMetaclass):
    """
    This one is actually a mixin, not a monkey-patch like the other two
    """
    bound_value = None

    class ViewMode(ViewModeEnum):
        FORM = auto()  # Render to form field
        TABLE_ROW = auto()  # Render to table tr
        TABLE_HEAD = auto()  # Render to table header

    df_control_data = fields.SerializerMethodField(display=DisplayMode.HIDDEN)

    """
    we're currently using two additional headers for axios:
    'x-viewmode': 'TABLE_ROW' - tells DF what viewMode to use for rendering the response
    'x-pagination': 1 - tells DRF to paginate (or not) the result
    """
    def __init__(self, *args, view_mode: 'ViewModeSerializer.ViewMode' = None,
                 view_mode_list: 'ViewModeListSerializer.ViewMode' = None,
                 **kwds
                 ):
        super().__init__(*args, **kwds)
        if not view_mode and self.request and 'HTTP_X_VIEWMODE' in self.request.META:
            view_mode = self.ViewMode[self.request.META['HTTP_X_VIEWMODE']]
        self.set_view_mode(view_mode)
        self.view_mode_list = view_mode_list

    def __new__(cls, *args, **kwargs):
        from .listserializer import ViewModeListSerializer

        view_mode_list = kwargs.pop('view_mode_list', None)
        res = super().__new__(cls, *args, **kwargs)
        if isinstance(res, ListSerializer):
            res = ViewModeListSerializer.mixin_to_serializer(view_mode_list, res)
        return res

    def set_bound_value(self, value: Dict[Any, Any]):
        self.bound_value = value

    @property
    def request(self: '_ViewModeBoundSerializer'):
        if self.context and 'view' in self.context and self.context['view'].request:
            return self.context['view'].request
        return None

    @property
    def is_rendering_as_table(self):
        """
        Overrides RenderMixin's implementation
        :return:
        """
        return self.view_mode in (ViewModeSerializer.ViewMode.TABLE_ROW, ViewModeSerializer.ViewMode.TABLE_HEAD)

    @property
    def render_fields(self: '_ViewModeBoundSerializer'):
        this = self

        class BoundSerializerRenderFields(SerializerRenderFields):

            @property
            def fields(self):
                actions = list(this.actions.renderable_actions(this))
                if any(action.position == TablePosition.ROW_START for action in actions):
                    yield SerializerRenderFields.ActionField(actions, TablePosition.ROW_START)

                for f in this.fields.values():
                    if f.display_table != DisplayMode.SUPPRESS:
                        yield f

                if any(action.position == TablePosition.ROW_END for action in actions):
                    yield SerializerRenderFields.ActionField(actions, TablePosition.ROW_END)

        return BoundSerializerRenderFields()

    @property
    def render_actions(self: '_ViewModeBoundSerializer'):
        this = self

        class BoundSerializerRenderActions(SerializerRenderActions):

            @property
            def actions(self):
                return this.actions

        return BoundSerializerRenderActions()

    def component_params(self: '_ViewModeBoundSerializer', output_json: bool = True):
        params = {
            'guid': self.uuid,
            'titles': self.form_titles,
            'columns': self.render_fields.columns.as_field_def(),  # todo: we need a self.setviewmode(header_row)
            'actions': self.render_actions.table.as_action_def(),
            'row-properties': self.render_fields.properties.as_name(),
            'record': None if self.parent else self.data
        }
        return convert_to_json_if(params, output_json)

    def get_df_control_data(self: '_ViewModeBoundSerializer', row):
        """
        Returns any additional data needed for rendering or operating the serializer on the client, such as presence of
        action buttons, thir parameters, CSS, etc.

          deprecates row_css_style and df_prev_link

        :param row: row data to consider when presenting the return data
        :return: dict of settings for actions and row-related data
        """
        return dict(
            row_css_style=self.get_row_css_style(row),
            actions=dict(
                filter(lambda x: x[1] is not None,
                       (action.to_component_params(row, self) for action in self.render_actions.table.actions))
            )
        )

    @classmethod
    def get_reverse_url(cls, view_name, request):
        return reverse(view_name + '-detail', format='json', request=request)


# noinspection PyAbstractClass
class _ViewModeBoundSerializer(ViewModeSerializer, RenderMixin, ActionMixin, Serializer):
    """
    Dummy class just for type hinting
    """

    class FakeActionsList(list):

        def renderable_actions(self, _unused):
            return self

    actions = FakeActionsList()
