import collections
import uuid as uuid_module
from typing import Iterable

from rest_framework.serializers import Serializer
from rest_framework.templatetags import rest_framework as drftt
from .action import Actions, FieldChangeAction


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


class ActionMixin(object):
    """
    Used in fields allowing declaration of actions that happen when field values change
    """

    def __init__(self, *args, actions: Actions = None, **kwargs):
        super().__init__(*args, **kwargs)
        act = actions or Actions()
        act.actions.extend(getattr(self, 'actions', Actions()).actions)
        # Obtain a personalised list of actions
        self.actions = act.get_resolved_copy(self)


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
