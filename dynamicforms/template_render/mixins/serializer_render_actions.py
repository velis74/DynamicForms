"""
Class that contains renderable fields for the templates.
The class provides transformation functionality
"""

from typing import Iterable

from dynamicforms.action import TableAction


class SerializerRenderActions(object):
    @property
    def actions(self) -> Iterable[TableAction]:
        raise NotImplementedError("You must implement the actions property in your serializer render_actions method")

    def as_action_def(self):
        res = {action.name: action.as_component_def() for action in self.actions}
        return res

    def __aiter__(self):
        return self.actions
