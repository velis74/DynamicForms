"""
Class that contains renderable fields for the templates.
The class provides transformation functionality
"""

from typing import Iterable

from django.utils.translation import ugettext_lazy as _

from dynamicforms.action import TableAction, TablePosition
from dynamicforms.mixins import DisplayMode


class SerializerRenderActions(object):
    @property
    def actions(self) -> Iterable[TableAction]:
        raise NotImplementedError('You must implement the actions property in your serializer render_actions method')

    def as_action_def(self):
        res = {action.name: dict(name=action.name, label=action.label, title=action.title, icon=action.icon,
                                 btn_classes=action.btn_classes, position=action.position.name,
                                 field_name=action.field_name
                                 )
               for action in self.actions}
        return res

    @property
    def table(self) -> 'SerializerRenderActions':
        """
        Returns actions that are TableActions - they are applicable to ViewMode.TABLE
        """
        this = self

        class BoundVisibleSerializerRenderFields(SerializerRenderActions):
            @property
            def actions(self):
                for action in this.actions:
                    if isinstance(action, TableAction):
                        yield action

        return BoundVisibleSerializerRenderFields()

    def __aiter__(self):
        return self.actions
