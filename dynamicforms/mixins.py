import collections
import re
import uuid as uuid_module
from datetime import datetime
from enum import IntEnum
from typing import Any, Optional

from django.utils import timezone
from rest_framework.fields import ChoiceField, DateField, TimeField
from rest_framework.relations import ManyRelatedField, RelatedField
from rest_framework.serializers import ListSerializer
from rest_framework.templatetags import rest_framework as drftt

from .action import Actions


class DisplayMode(IntEnum):
    SUPPRESS = 1  # Field will be entirely suppressed. it will not render (not even to JSON) and will not parse for PUT
    HIDDEN = 5  # Field will render as <input type="hidden"> or <tr data-field_name>
    INVISIBLE = 8  # Field will render completely, but with display: none. Equal to setting its style = {display: none}
    FULL = 10  # Field will render completely


class RenderMixin(object):
    """
    Is used in fields and serializers, so every field and serializer gets its unique id. Also to specify where and how
    fields should render.

    In form where serializer is used, id is serializers uuid. Table with list of records has id »list-serializer.uuid«,
    in dialog id is »dialog-{serializer.uuid}« and save button's id on dialog is »save-{serializer.uuid}«

    Similar for fields: All inputs in HTML get id from field.uuid. Div that contains all that belongs to the field has
    »container-{field.uuid}« for id, label has »label-{field.uuid}« and help text (if exists) has »help-{field.uuid}«
    for id.

    Used for rendering individual field to table view
    """

    def __init__(self, *args, uuid: uuid_module.UUID = None,
                 display: DisplayMode = None,  # Leave at default
                 display_table: DisplayMode = None,  # Leave at default
                 display_form: DisplayMode = None,  # Leave at default
                 table_classes: str = '',
                 **kwargs):
        """

        :param args: passed on to inherited constructors
        :param uuid: custom specified field UUID. if not specified, it will be assigned automatically
        :param display: see DisplayMode enum. Specifies how field will render. Leave at None for default (FULL)
            display_form and display_table also accepted for better granularity
        :param table_classes: css classes to add to the table column
        :param kwargs: passed on to inherited constructors
        """
        super().__init__(*args, **kwargs)
        self.uuid = uuid or uuid_module.uuid1()
        self.display_table = display_table or display or DisplayMode.FULL
        self.display_form = display_form or display or DisplayMode.FULL
        self.table_classes = table_classes

    def set_display(self, value):
        self.display_form = self.display_table = value

    display = property(lambda self: self.display_form, set_display)

    # noinspection PyUnusedLocal
    def render_to_table(self, value, row_data):
        """
        Renders field value for table view

        :param value: field value
        :param row_data: data for entire row (for more complex renderers)
        :return: rendered value for table view
        """
        get_queryset = getattr(self, 'get_queryset', None)
        if isinstance(self, RelatedField) or get_queryset:
            # shortcut for getting display value for table without actually getting the entire table into choices
            qs = get_queryset()
            try:
                qs = qs.filter(pk=value)
                choices = {self.to_representation(item): self.display_value(item) for item in qs}
            except:
                choices = getattr(self, 'choices', {})
        elif isinstance(self, ManyRelatedField):
            # if value is a list, we're dealing with ManyRelatedField, so let's not do that
            cr = self.child_relation
            return ', '.join((cr.display_value(item) for item in cr.get_queryset().filter(pk__in=value)))
        else:
            choices = getattr(self, 'choices', {})

        if isinstance(value, collections.Hashable) and value in choices:
            # choice field: let's render display names, not values
            return drftt.format_value(choices[value])
        return drftt.format_value(value)


class ActionMixin(object):
    """
    Used in fields allowing declaration of actions that happen when field values change
    """

    def __init__(self, *args, actions: Actions = None, **kwargs):
        super().__init__(*args, **kwargs)
        act = actions or Actions(None)
        act.actions.extend(getattr(self, 'actions', Actions()).actions)
        # Obtain a personalised list of actions
        self.actions = act.get_resolved_copy(self)


class NullChoiceMixin(object):
    """
    Declaring ChoiceField's null_choice_text
      (what should be rendered for "no selection"; DRF's default is ---------)
      We also support user declaring a choice with None value and a different text (see hidden fields example)
    """

    @property
    def null_choice_text(self):
        res = '--------'
        if isinstance(self, ChoiceField) and not getattr(self, 'get_queryset', None):
            # Only do this for true ChoiceFields. ReladedFields would run a query here
            # Possibly we will at some point have to enable this for relatedfields too
            for opt in self.iter_options():
                if opt.start_option_group or opt.end_option_group:
                    pass
                elif opt.value is None:
                    res = opt.display_text
        return res

    def iter_options_bound(self, value):
        return super().iter_options()


class HiddenFieldMixin(RenderMixin):

    def __init__(self, *args, **kwargs):
        kwargs.setdefault('display_table', DisplayMode.SUPPRESS)
        super().__init__(*args, **kwargs)


class RelatedFieldAJAXMixin(object):

    def __init__(self, *args, url_reverse: Optional[str] = None, placeholder: Optional[str] = None,
                 additional_parameters: Optional[dict] = None, query_field: str = 'query', **kwargs):
        """
        Allows us to use AJAX to populate select2 options instead of pre-populating at render time

        :param args:
        :param url_reverse: reverse url to ViewSet providing the JSON data
        :param placeholder: select2 placeholder to display until user selects a value
        :param additional_parameters: additional parameters to be sent to ViewSet as part of the query
        :param query_field: field against which user search will be performed
        :param kwargs:
        """
        super().__init__(*args, **kwargs)
        self.url_reverse = url_reverse
        self.placeholder = placeholder
        self.additional_parameters = additional_parameters
        self.query_field = query_field

    @property
    def additional_parameters_urlencoded(self):
        from django.utils.http import urlencode
        return '?' + urlencode(self.additional_parameters)

    # noinspection PyUnresolvedReferences
    def iter_options_bound(self, value):
        if self.url_reverse:
            qry = self.get_queryset()
            try:
                qry = qry.filter(pk=value)
                return [dict(value=value, display_text=self.display_value(qry.first()))]
            except:
                return []
        return super().iter_options()


class NaturalDateTimeMixin(object):
    """
    Used for rendering datetime in human natural style (e.g.: 1 hour, 10 minutes ago)
    """

    def __init__(self, *args, table_format: str = '', **kwargs) -> None:
        """

        :param args:
        :param table_format: Format for datetime rendering in table (non editable). If format is %N:{precision},
            datetime will render in natural style with {precision} depth
        :param kwargs:
        """
        super().__init__(*args, **kwargs)
        self.table_format = table_format

    # noinspection PyUnresolvedReferences
    def to_representation(self, value: Any) -> Any:
        if not value:
            return None

        if isinstance(value, str):
            return value

        if isinstance(self.parent.parent, ListSerializer):
            output_format = getattr(self, 'table_format', None)
            if output_format is not None and re.match(r'%N:\d+', output_format):
                imported = False
                try:
                    # This library (will-natural) is used because is the only one we could find that adds text saying
                    # when is this datetime ("ago" or "from now") and have the possibility to set max precision
                    from natural.date import duration
                    imported = True
                except:
                    print('Install library for natural presentation of date (pip install will-natural)')

                if imported:
                    if isinstance(self, DateField):
                        now = timezone.now().date()
                    elif isinstance(self, TimeField):
                        now = datetime.now()
                        value = datetime.now().replace(hour=value.hour, minute=value.minute, second=value.second,
                                                       microsecond=value.microsecond)
                    else:
                        now = timezone.now()

                    # noinspection PyUnboundLocalVariable
                    return duration(value, now=now, precision=int(output_format.split(':')[1]))
        return super().to_representation(value)


class TimeFieldMixin(NaturalDateTimeMixin):

    def __init__(self, *args, table_format: str = '', **kwargs) -> None:
        super().__init__(*args, table_format=table_format, **kwargs)


class DateFieldMixin(NaturalDateTimeMixin):

    def __init__(self, *args, table_format: str = '', **kwargs) -> None:
        super().__init__(*args, table_format=table_format, **kwargs)


class DateTimeFieldMixin(NaturalDateTimeMixin):

    def __init__(self, *args, table_format: str = '', **kwargs) -> None:
        super().__init__(*args, table_format=table_format, **kwargs)
