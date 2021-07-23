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
    def __init__(self):
        self.child = None

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

    def component_params(self: '_ViewModeBoundListSerializer', output_json: bool = True, data=None):
        res = self.child.component_params(output_json=False)

        if self.paginator:
            res['rows'] = data or self.paginator.get_paginated_response(self.data).data
        else:
            res['rows'] = dict(prev=None, next=None, results=data or self.data)

        res['list_url'] = self.reverse_url
        return convert_to_json_if(res, output_json)

    uuid = property(lambda self: self.child.uuid)  # propagate original serializer's uuid to list serializer

    @classmethod
    def get_reverse_url(cls, view_name, request):
        return reverse(view_name + '-list', format='json', request=request)

    def apply_component_context(self, request, paginator):
        # Different to ViewModeSerializer.get_component_context - which is a class method creating the instances
        # this one will decorate existing instance with the appropriate values needed for rendering
        # in all other respects, they are the same
        self.child.apply_component_context(request, paginator)
        self.view_mode = ViewModeListSerializer.ViewMode.TABLE
        self.reverse_url = self.get_reverse_url(self.child.template_context['url_reverse'], request)
        self.paginator = paginator
        if paginator:
            base_url = paginator.base_url.split('?', 1)
            paginator.base_url = self.reverse_url + (('?' + base_url[1]) if len(base_url) == 2 else '')


# noinspection PyAbstractClass
class _ViewModeBoundListSerializer(ViewModeListSerializer, ListSerializer):
    """
    Dummy class just for type hinting
    """
    pass
