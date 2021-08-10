"""
Class that contains renderable fields for the templates.
The class provides transformation functionality
"""

from typing import Iterable

from django.utils.translation import ugettext_lazy as _

from dynamicforms.action import TableAction, TablePosition
from dynamicforms.mixins import DisplayMode, FieldAlignment


class SerializerRenderFields(object):
    @property
    def fields(self):
        raise NotImplementedError('You must implement the fields property in your serializer render_fields method')

    def __aiter__(self):
        return self.fields

    class ActionField(object):
        def __init__(self, actions: Iterable[TableAction], pos: TablePosition):
            from collections.abc import Iterable as Itr
            if not isinstance(actions, Itr) or not all(isinstance(action, TableAction) for action in actions):
                raise AssertionError('Actions should be an iterable of TableAction')
            actions = [action for action in actions if action.position == pos]
            self.position = pos
            self.actions = actions
            self.field_name = '#actions-' + pos.name.lower()
            self.label = _('Actions')
            self.table_classes = ''
            self.display_table = DisplayMode.FULL
            self.alignment = FieldAlignment.LEFT
            self.render_params = {}

        # noinspection PyMethodMayBeStatic
        def ordering(self):
            return ''

        def as_component_def(self: 'ActionField') -> dict:
            return dict(name=str(self.field_name), label=str(self.label),
                        align='right' if self.alignment == FieldAlignment.DECIMAL else self.alignment.name.lower(),
                        table_classes=self.table_classes, ordering=self.ordering(), visibility=self.display_table.name,
                        render_params=self.render_params
                        )
