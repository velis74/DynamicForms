from enum import auto
from typing import Dict, List

from django.template import loader
from rest_framework.reverse import reverse
from rest_framework.serializers import ListSerializer

from dynamicforms.mixins import FieldRenderMixin

from .base import ViewModeBase
from .render_mode_enum import ViewModeEnum
from .util import convert_to_json_if


class ViewModeListSerializer(ViewModeBase, FieldRenderMixin, ListSerializer):
    bound_value = None

    class ViewMode(ViewModeEnum):
        TABLE = auto()  # Render to full table with header, filter, rows

    def __init__(self, *args, **kwargs):
        self.child = None
        kwargs.setdefault("display_table", kwargs["child"].display_table)
        kwargs.setdefault("display_form", kwargs["child"].display_form)
        super().__init__(*args, **kwargs)

    def set_bound_value(self, value: List[Dict]):
        self.bound_value = value

    def render_table(self: "_ViewModeBoundListSerializer"):
        template = loader.get_template("template_render/full_table.html")
        context = dict(serializer=self, columns=self.render_fields)
        return template.render(context)

    @property
    def render_fields(self: "_ViewModeBoundListSerializer"):
        return self.child.render_fields

    @property
    def render_actions(self: "_ViewModeBoundListSerializer"):
        return self.child.render_actions

    def component_params(self: "_ViewModeBoundListSerializer", output_json: bool = True, data=None):
        res = self.child.component_params(output_json=False)

        if self.paginator:
            res["rows"] = data or self.paginator.get_paginated_response(self.data).data
        else:
            res["rows"] = dict(prev=None, next=None, results=data or self.data)

        res["list_url"] = self.reverse_url
        return convert_to_json_if(res, output_json)

    # propagate original serializer's uuid to list serializer
    uuid = property(lambda self: self.child.uuid, lambda self, value: setattr(self.child, "uuid", value))

    @classmethod
    def get_reverse_url(cls, view_name, request, kwargs=None):
        if kwargs:
            kwargs = kwargs.copy()
            kwargs.pop("pk", None)
        return reverse(view_name + "-list", format="json", request=request, kwargs=kwargs)

    def apply_component_context(self, request=None, paginator=None):
        # Different to ViewModeSerializer.get_component_context - which is a class method creating the instances
        # this one will decorate existing instance with the appropriate values needed for rendering
        # in all other respects, they are the same
        request = request or self.request
        paginator = paginator or self.context.get("view", type("NoView", (object,), dict(paginator=None))).paginator

        self.child.apply_component_context(request, paginator)
        self.view_mode = ViewModeListSerializer.ViewMode.TABLE
        self.reverse_url = self.get_reverse_url(
            self.child.template_context["url_reverse"],
            request,
            self.child.template_context.get("url_reverse_kwargs", self.child.default_url_reverse_kwargs),
        )
        self.paginator = paginator
        if paginator:
            base_url = paginator.base_url.split("?", 1)
            paginator.base_url = self.reverse_url + (("?" + base_url[1]) if len(base_url) == 2 else "")

    @property
    def request(self: "_ViewModeBoundListSerializer"):
        if self.context and "view" in self.context and self.context["view"].request:
            return self.context["view"].request
        elif self.child:
            return self.child.request
        return None

    def as_component_def(self: "DFField") -> dict:  # noqa
        if hasattr(self.child, "as_component_def_table"):
            return self.child.as_component_def_table
        res = super().as_component_def()
        res["render_params"]["form_component_name"] = "DList"
        self.child.apply_component_context()
        res["render_params"]["form_component_def"] = self.child.component_params(output_json=False)
        return res


# noinspection PyAbstractClass
class _ViewModeBoundListSerializer(ViewModeListSerializer, ListSerializer):
    """
    Dummy class just for type hinting
    """

    pass
