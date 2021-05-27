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

    def as_field_def(self):
        res = [dict(name=str(field.field_name), label=str(field.label),
                    align='right' if field.alignment == FieldAlignment.DECIMAL else field.alignment.name.lower(),
                    table_classes=field.table_classes, ordering=field.ordering(), visibility=field.display_table.name,
                    render_params=field.render_params
                    )
               for field in self.fields]
        return res

    def as_name(self):
        res = [field.field_name for field in self.fields]
        return res

    @property
    def columns(self) -> 'SerializerRenderFields':
        """
        Returns fields that need to be rendered as columns in table, either fully visible or hidden
        This is as opposed to rendering the fields into data-field_name properties for the HIDDEN fields(see properties)
        """
        this = self

        class BoundVisibleSerializerRenderFields(SerializerRenderFields):
            @property
            def fields(self):
                for fld in this.fields:
                    if fld.display_table in (DisplayMode.INVISIBLE, DisplayMode.FULL):
                        yield fld

        return BoundVisibleSerializerRenderFields()

    @property
    def properties(self) -> 'SerializerRenderFields':
        """
        Returns fields that need to be rendered as data-field_name properties in tr
        This is as opposed to rendering the table columns
        """
        this = self

        class BoundVisibleSerializerRenderFields(SerializerRenderFields):
            @property
            def fields(self):
                for fld in this.fields:
                    if fld.display_table == DisplayMode.HIDDEN:
                        yield fld

        return BoundVisibleSerializerRenderFields()

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
