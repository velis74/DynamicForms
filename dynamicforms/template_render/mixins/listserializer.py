from enum import auto
from typing import Dict, List, Optional

from django.template import loader
from rest_framework.reverse import reverse
from rest_framework.serializers import ListSerializer

from .base import ViewModeBase
from .render_mode_enum import ViewModeEnum
from .util import convert_to_json_if


class ViewModeListSerializer(ViewModeBase):
    bound_value = None

    class ViewMode(ViewModeEnum):
        TABLE = auto()  # Render to full table with header, filter, rows

    # noinspection PySuperArguments,PyUnresolvedReferences
    @staticmethod
    def mixin_to_serializer(view_mode: 'ViewModeListSerializer.ViewMode', serializer: ListSerializer,
                            value: Optional[List[Dict]] = None):
        serializer.__class__ = type(
            'ViewMode' + serializer.child.__class__.__name__, (ViewModeListSerializer, serializer.__class__), {}
        )
        super(ViewModeListSerializer, serializer).set_view_mode(view_mode)
        serializer.set_bound_value(value)
        return serializer

    def set_bound_value(self, value: List[Dict]):
        self.bound_value = value

    def render_table(self: '_ViewModeBoundListSerializer'):
        template = loader.get_template('template_render/full_table.html')
        context = dict(serializer=self, columns=self.render_fields)
        return template.render(context)

    @property
    def render_fields(self: '_ViewModeBoundListSerializer'):
        return self.child.render_fields

    @property
    def render_actions(self: '_ViewModeBoundListSerializer'):
        return self.child.render_actions

    def component_params(self: '_ViewModeBoundListSerializer'):
        res = self.child.component_params(output_json=False)
        res['rows'] = self.paginator.get_paginated_response(self.data).data
        res['list_url'] = self.reverse_url
        return convert_to_json_if(res, True)

    uuid = property(lambda self: self.child.uuid)  # propagate original serializer's uuid to list serializer

    @classmethod
    def get_reverse_url(cls, view_name, request):
        return reverse(view_name + '-list', format='json', request=request)


# noinspection PyAbstractClass
class _ViewModeBoundListSerializer(ViewModeListSerializer, ListSerializer):
    """
    Dummy class just for type hinting
    """
    pass
