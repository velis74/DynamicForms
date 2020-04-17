import uuid as uuid_module
from enum import IntEnum
from typing import Hashable

from rest_framework.fields import Field as DrfField
from rest_framework.relations import ManyRelatedField, RelatedField
from rest_framework.templatetags import rest_framework as drftt

from dynamicforms.settings import DYNAMICFORMS


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
                 display: DisplayMode = None,  # None == Leave at default
                 display_table: DisplayMode = None,  # None == Leave at default
                 display_form: DisplayMode = None,  # None == Leave at default
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
        # noinspection PyUnresolvedReferences
        self.display_table = (
            display_table or display
            or (DisplayMode.FULL if not getattr(self, 'write_only', False) else DisplayMode.SUPPRESS)
        )
        self.display_form = display_form or display or DisplayMode.FULL
        self.table_classes = table_classes

    @property
    def is_rendering_to_list(self):
        """
        reports whether we are currently rendering to table or to single record
        :return:
        """
        try:
            # noinspection PyUnresolvedReferences
            if self.parent.parent:
                return True
        except:
            pass
        return False

    @property
    def is_rendering_to_html(self):
        try:
            # noinspection PyUnresolvedReferences
            return self.context['format'] == 'html'
        except:
            pass
        return False

    # noinspection PyUnresolvedReferences
    def use_pk_only_optimization(self):
        """
        Overrides DRF RelatedField's method. It True is returned then value passed for serailization will be PK value
        only, not entire relation object
        :return:
        """
        if self.is_rendering_to_list and self.is_rendering_to_html:
            return False
        return super().use_pk_only_optimization()

    # noinspection PyUnresolvedReferences
    def to_representation(self, value):
        """
        Overrides DRF Field's to_representation.
        Note that this is also called for the entire record as well as the serializer also is a Field descendant
        :param value: value to serialize
        :return: serialized value
        """
        if self.is_rendering_to_list and self.is_rendering_to_html:
            return self.render_to_table(value, self.parent.instance)
        return super().to_representation(value)

    def set_display(self, value):
        self.display_form = self.display_table = value

    display = property(lambda self: self.display_form, set_display)

    # noinspection PyUnusedLocal, PyUnresolvedReferences
    def render_to_table(self, value, row_data):
        """
        Renders field value for table view

        :param value: field value
        :param row_data: data for entire row (for more complex renderers)
        :return: rendered value for table view
        """
        get_queryset = getattr(self, 'get_queryset', None)
        if isinstance(self, RelatedField) or get_queryset:
            return self.display_value(value)
        elif isinstance(self, ManyRelatedField):
            # if value is a list, we're dealing with ManyRelatedField, so let's not do that
            print('WARNING/TODO: ManyRelatedField lookup wasn\'t fixed with the rest of the code for lack of examples')
            cr = self.child_relation
            return ', '.join((cr.display_value(item) for item in cr.get_queryset().filter(pk__in=value)))
        else:
            choices = getattr(self, 'choices', {})

        # Now that we got our choices for related & choice fields, let's first get the value as it would be by DRF
        value = super().to_representation(value)

        if isinstance(value, Hashable) and value in choices:
            # choice field: let's render display names, not values
            value = choices[value]
        if value is None:
            return DYNAMICFORMS.null_text_table

        return drftt.format_value(value)

    def validate_empty_values(self: DrfField, data):
        # noinspection PyUnresolvedReferences
        res = super().validate_empty_values(data)

        # This is to fix a problem with calculated fields which was only solved in DRF 3.10.
        # Forces validation and inclusion of the field into validated data. See comment in original function.
        if res == (True, None) and data is None and self.source == '*':
            return False, None
        return res
