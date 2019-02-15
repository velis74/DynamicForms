import collections
import uuid as uuid_module
from typing import List

from rest_framework.serializers import Serializer
from rest_framework.templatetags import rest_framework as drftt


class UUIDMixIn(object):
    """
    Is used in fields and serializers, so every field and serializer gets its unique id.

    In form where serializer is used, id is serializers uuid. Table with list of records has id »list-serializer.uuid«,
    in dialog id is »dialog-{serializer.uuid}« and save button's id on dialog is »save-{serializer.uuid}«

    Similar for fields: All inputs in HTML get id from field.uuid. Div that contains all that belongs to the field has
    »container-{field.uuid}« for id, label has »label-{field.uuid}« and help text (if exists) has »help-{field.uuid}«
    for id.
    """

    def __init__(self, *args, uuid: uuid_module.UUID = None, **kwargs):
        super().__init__(*args, **kwargs)
        self.uuid = uuid or uuid_module.uuid1()


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
    elif isinstance(ref, str) and '.' in ref:
        # This supports nested serializers and fields with . notation, e.g. master_serializer_field.child_field
        f = serializer
        for r in ref.split('.'):
            f = f[r]
        return f.uuid
    raise Exception('Unknown reference type for Action tracked field (%r)' % ref)


class Action(object):

    def __init__(self, tracked_fields: List[str], action_js: str):
        self.tracked_fields = tracked_fields
        self.action_js = action_js
        assert self.tracked_fields, 'When declaring an action, it must track at least one form field'
        assert self.action_js, 'When declaring action, it must declare action JavaScript to execute'

    @property
    def action_id(self):
        return id(self)

    def copy_and_resolve_reference(self, serializer: Serializer):
        return Action([_resolve_reference(serializer, f) for f in self.tracked_fields], self.action_js)


class ActionMixin(object):
    """
    Used in fields allowing declaration of actions that happen when field values change
    """

    def __init__(self, *args, actions: List['Action'] = None, **kwargs):
        super().__init__(*args, **kwargs)
        if not getattr(self, 'actions', None):
            self.actions = actions or []

    @property
    def action_register_js(self):
        """
        returns JavaScript function parameters needed for dynamicforms.registerFieldAction() function

        :return: List[{'tracked_fields': List[str], 'action_function': str}]
        """
        if isinstance(self, Serializer) and not hasattr(self, '_actions'):
            setattr(self, '_actions', [a.copy_and_resolve_reference(self) for a in (self.actions or [])])

            # remove actions from Field, move them to Serializer
            for field in self.fields.values():
                # field: ActionMixin
                self._actions.extend([a.copy_and_resolve_reference(self) for a in getattr(field, 'actions', [])])

            # Change all {field name}, Field to UUID references
            for action in self._actions:
                action.tracked_fields = [_resolve_reference(self, ref) for ref in action.tracked_fields]

        return self._actions


class RenderToTableMixin(object):
    """
    Used for rendering individual field to table view
    """

    def __init__(self, *args, visible_in_table: bool = True, table_classes: str = '', **kwargs):
        super().__init__(*args, **kwargs)
        self.visible_in_table = visible_in_table
        self.table_classes = table_classes

    def render_to_table(self, value, row_data):
        """
        Renders field value for table view

        :param value: field value
        :param row_data: data for entire row (for more complex renderers)
        :return: rendered value for table view
        """
        get_queryset = getattr(self, 'get_queryset', None)
        if get_queryset:
            # shortcut for getting display value for table without actually getting the entire table into choices
            qs = get_queryset()

            try:
                qs = qs.filter(pk=value)
                choices = { self.to_representation(item): self.display_value(item) for item in qs }
            except:
                choices = getattr(self, 'choices', {})
        else:
            choices = getattr(self, 'choices', {})

        if isinstance(value, list) and choices:
            # if value is a list, we're dealing with ManyRelatedField, so let's not do that
            return ', '.join((drftt.format_value(choices[v]) for v in value))
        elif isinstance(value, collections.Hashable) and value in choices:
            # choice field: let's render display names, not values
            return drftt.format_value(choices[value])
        return drftt.format_value(value)


class HiddenFieldMixin(RenderToTableMixin):

    def __init__(self, *args, visible_in_table: bool = True, **kwargs):
        super().__init__(*args, **kwargs)
        self.visible_in_table = False
