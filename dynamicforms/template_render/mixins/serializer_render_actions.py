"""
Class that contains renderable fields for the templates.
The class provides transformation functionality
"""

from typing import Iterable, Tuple, Type, Union

from dynamicforms.action import ActionBase, FormButtonAction, FormInitAction, TableAction


class SerializerRenderActions(object):
    @property
    def actions(self) -> Iterable[TableAction]:
        raise NotImplementedError('You must implement the actions property in your serializer render_actions method')

    def as_action_def(self):
        res = {action.name: action.as_component_def() for action in self.actions}
        return res

    def filter_actions(self, action_type: Union[Type[ActionBase], Tuple[Type[ActionBase], ...]]):
        this = self

        class BoundVisibleSerializerRenderFields(SerializerRenderActions):
            @property
            def actions(self):
                for action in this.actions:
                    if isinstance(action, action_type):
                        yield action

        return BoundVisibleSerializerRenderFields()

    @property
    def table(self) -> 'SerializerRenderActions':
        """
        Returns actions that are TableActions - they are applicable to ViewMode.TABLE
        """
        return self.filter_actions(TableAction)

    @property
    def form(self) -> 'SerializerRenderActions':
        """
        Returns actions that are defined for the form - they are applicable to ViewMode.FORM
        """
        return self.filter_actions((FormInitAction, FormButtonAction))

    def __aiter__(self):
        return self.actions
