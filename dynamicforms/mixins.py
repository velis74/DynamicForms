from typing import List
import uuid as uuid_module
from rest_framework.serializers import Serializer
from django.utils.safestring import mark_safe

# noinspection PyUnreachableCode
if False:
    from dynamicforms.serializers import ModelSerializer


class UUIDMixIn(object):
    """
    Is used in fields and serializers, so every field and serializer gets its unique id.

    In form where serializer is used, id is serializers uuid. Table with list of records has id »list-serializer.uuid«,
    in dialog id is »dialog-{serializer.uuid}« and save button's id on dialog is »save-{serializer.uuid}«

    Similar for fields: All inputs in HTML get id from field.uuid. Div that contains all that belongs to the field has
    »container-{field.uuid}« for id, label has »label-{field.uuid}« and help text (if exists) has »help-{field.uuid}«
    for id.
    """

    def __init__(self, *args, uuid: uuid_module.UUID=None, **kwargs):
        super().__init__(*args, **kwargs)
        self.uuid = uuid or uuid_module.uuid1()


class Action(object):

    def __init__(self, tracked_fields: List[str], action_js: str):
        self.tracked_fields = tracked_fields
        self.action_js = action_js
        assert self.tracked_fields, 'When declaring an action, it must track at least one form field'
        assert self.action_js, 'When declaring action, it must declare action JavaScript to execute'

    def to_json(self, serializer: 'ModelSerializer'):
        return dict(tracked_fields=self.tracked_fields, action_function=mark_safe(self.action_js))

    @property
    def action_id(self):
        return id(self)


def _resolve_reference(serializer: Serializer, ref):
    if isinstance(ref, uuid_module.UUID):
        return ref
    elif isinstance(ref, UUIDMixIn):
        # TODO unit tests!!!
        # TODO test what happens if the Field instance given is from another serializer
        # TODO test what happens when Field instance is actually a Serializer (when should onchange trigger for it?)
        return ref.uuid
    elif isinstance(ref, str) and ref in serializer.fields:
        return serializer[ref].uuid
    raise Exception('Unknown reference type for Action tracked field (%r)' % ref)


class ActionMixin(object):
    """
    Used in fields allowing declaration of actions that happen when field values change
    """
    def __init__(self, *args, actions: List['Action']=None, **kwargs):
        super().__init__(*args, **kwargs)
        self.actions = actions or []

    @property
    def action_register_js(self):
        """
        returns JavaScript function parameters needed for dynamicforms.registerFieldAction() function

        :return: List[{'tracked_fields': List[str], 'action_function': str}]
        """
        if isinstance(self, Serializer) and not hasattr(self, '_actions'):
            setattr(self, '_actions', [])

            # remove actions from Field, move them to Serializer
            for field in self.fields.values():
                # field: ActionMixin
                self._actions.extend(field.actions)

            # Change all {field name}, Field to UUID references
            for action in self._actions:
                action.tracked_fields = [_resolve_reference(self, ref) for ref in action.tracked_fields]

        return self._actions
