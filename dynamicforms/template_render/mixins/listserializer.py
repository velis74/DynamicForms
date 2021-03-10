from enum import auto
from typing import Dict, List, Optional

from rest_framework.serializers import ListSerializer

from .base import ViewModeBase
from .render_mode_enum import ViewModeEnum
from django.template import loader


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
        context = dict(columns=self.render_fields)
        return template.render(context)

    @property
    def render_fields(self: '_ViewModeBoundListSerializer'):
        return self.child.render_fields


# noinspection PyAbstractClass
class _ViewModeBoundListSerializer(ViewModeListSerializer, ListSerializer):
    """
    Dummy class just for type hinting
    """
    pass
