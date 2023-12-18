"""
Class that contains renderable fields for the templates.
The class provides transformation functionality
"""
import uuid

from typing import Iterable

from django.utils.translation import gettext_lazy as _

from dynamicforms.action import TableAction, TablePosition
from dynamicforms.mixins import DisplayMode, FieldAlignment


class SerializerRenderFields(object):
    @property
    def fields(self):
        raise NotImplementedError("You must implement the fields property in your serializer render_fields method")

    def __aiter__(self):
        return self.fields

    class ActionField(object):
        def __init__(self, actions: Iterable[TableAction], pos: TablePosition):
            from collections.abc import Iterable as Itr

            if not isinstance(actions, Itr) or not all(isinstance(action, TableAction) for action in actions):
                raise AssertionError("Actions should be an iterable of TableAction")
            actions = [action for action in actions if action.position == pos]
            self.uuid = uuid.uuid1()
            self.position = pos
            self.actions = actions
            self.field_name = "#actions-" + pos.name.lower()
            self.label = _("Actions")
            self.table_classes = ""
            self.display_table = DisplayMode.FULL
            self.alignment = FieldAlignment.LEFT
            self.render_params = {}

        # noinspection PyMethodMayBeStatic
        def ordering(self):
            return ""

        def as_component_def(self) -> dict:
            return dict(
                uuid=self.uuid,
                name=str(self.field_name),
                label=str(self.label),
                read_only=False,
                alignment="right" if self.alignment == FieldAlignment.DECIMAL else self.alignment.name.lower(),
                table_classes=self.table_classes,
                ordering=self.ordering(),
                render_params=self.render_params,
                help_text="",
                visibility=dict(table=self.display_table.value),
                allow_null=False,
            )
