import warnings
from typing import Optional
from uuid import UUID

import rest_framework
from rest_framework import fields, relations

from .action import Actions
from .mixins import (ActionMixin, AllowTagsMixin, BooleanFieldMixin, DateFieldMixin, DateTimeFieldMixin, DisplayMode,
                     FieldHelpTextMixin, HiddenFieldMixin, NullChoiceMixin, RelatedFieldAJAXMixin, RenderMixin,
                     TimeFieldMixin)
from .settings import version_check


class BooleanField(BooleanFieldMixin, RenderMixin, ActionMixin, FieldHelpTextMixin, fields.BooleanField):

    def __init__(self, read_only=False, write_only=False, required=None, default=fields.empty, initial=fields.empty,
                 source=None, label=None, help_text=None, style=None, error_messages=None, validators=None,
                 actions: Actions = None, uuid: UUID = None, display: DisplayMode = None,
                 display_table: DisplayMode = None, display_form: DisplayMode = None, table_classes: str = '', **kw):
        kwargs = {k: v for k, v in locals().items() if not k.startswith(('__', 'self', 'kw'))}
        kwargs.update(kw)
        super().__init__(**kwargs)


class NullBooleanField(RenderMixin, ActionMixin, FieldHelpTextMixin, fields.NullBooleanField):

    def __init__(self, read_only=False, write_only=False, required=None, default=fields.empty, initial=fields.empty,
                 source=None, label=None, help_text=None, style=None, error_messages=None, validators=None,
                 actions: Actions = None, uuid: UUID = None, display: DisplayMode = None,
                 display_table: DisplayMode = None, display_form: DisplayMode = None, table_classes: str = '', **kw):
        kwargs = {k: v for k, v in locals().items() if not k.startswith(('__', 'self', 'kw'))}
        kwargs.update(kw)
        super().__init__(**kwargs)


class CharField(RenderMixin, ActionMixin, FieldHelpTextMixin, fields.CharField):

    def __init__(self, read_only=False, write_only=False, required=None, default=fields.empty, initial=fields.empty,
                 source=None, label=None, help_text=None, style=None, error_messages=None, validators=None,
                 allow_null=False, actions: Actions = None, uuid: UUID = None, display: DisplayMode = None,
                 display_table: DisplayMode = None, display_form: DisplayMode = None, table_classes: str = '', **kw):
        kwargs = {k: v for k, v in locals().items() if not k.startswith(('__', 'self', 'kw'))}
        kwargs.update(kw)
        super().__init__(**kwargs)


class EmailField(RenderMixin, ActionMixin, FieldHelpTextMixin, fields.EmailField):

    def __init__(self, read_only=False, write_only=False, required=None, default=fields.empty, initial=fields.empty,
                 source=None, label=None, help_text=None, style=None, error_messages=None, validators=None,
                 allow_null=False, actions: Actions = None, uuid: UUID = None, display: DisplayMode = None,
                 display_table: DisplayMode = None, display_form: DisplayMode = None, table_classes: str = '', **kw):
        kwargs = {k: v for k, v in locals().items() if not k.startswith(('__', 'self', 'kw'))}
        kwargs.update(kw)
        super().__init__(**kwargs)


class RegexField(RenderMixin, ActionMixin, FieldHelpTextMixin, fields.RegexField):

    def __init__(self, regex, read_only=False, write_only=False, required=None, default=fields.empty,
                 initial=fields.empty, source=None, label=None, help_text=None, style=None, error_messages=None,
                 validators=None, allow_null=False, actions: Actions = None, uuid: UUID = None,
                 display: DisplayMode = None, display_table: DisplayMode = None, display_form: DisplayMode = None,
                 table_classes: str = '', **kw):
        kwargs = {k: v for k, v in locals().items() if not k.startswith(('__', 'self', 'kw'))}
        kwargs.update(kw)
        super().__init__(**kwargs)


class SlugField(RenderMixin, ActionMixin, FieldHelpTextMixin, fields.SlugField):

    def __init__(self, allow_unicode=False, read_only=False, write_only=False, required=None, default=fields.empty,
                 initial=fields.empty, source=None, label=None, help_text=None, style=None, error_messages=None,
                 validators=None, allow_null=False, actions: Actions = None, uuid: UUID = None,
                 display: DisplayMode = None, display_table: DisplayMode = None, display_form: DisplayMode = None,
                 table_classes: str = '', **kw):
        kwargs = {k: v for k, v in locals().items() if not k.startswith(('__', 'self', 'kw'))}
        kwargs.update(kw)
        # noinspection PyUnresolvedReferences
        if not version_check(rest_framework.VERSION, '3.6.4'):
            kwargs.pop('allow_unicode', None)
        super().__init__(**kwargs)


class URLField(RenderMixin, ActionMixin, FieldHelpTextMixin, fields.URLField):

    def __init__(self, read_only=False, write_only=False, required=None, default=fields.empty, initial=fields.empty,
                 source=None, label=None, help_text=None, style=None, error_messages=None, validators=None,
                 allow_null=False, actions: Actions = None, uuid: UUID = None, display: DisplayMode = None,
                 display_table: DisplayMode = None, display_form: DisplayMode = None, table_classes: str = '', **kw):
        kwargs = {k: v for k, v in locals().items() if not k.startswith(('__', 'self', 'kw'))}
        kwargs.update(kw)
        super().__init__(**kwargs)


class UUIDField(RenderMixin, ActionMixin, FieldHelpTextMixin, fields.UUIDField):

    def __init__(self, read_only=False, write_only=False, required=None, default=fields.empty, initial=fields.empty,
                 source=None, label=None, help_text=None, style=None, error_messages=None, validators=None,
                 allow_null=False, actions: Actions = None, uuid: UUID = None, display: DisplayMode = None,
                 display_table: DisplayMode = None, display_form: DisplayMode = None, table_classes: str = '', **kw):
        kwargs = {k: v for k, v in locals().items() if not k.startswith(('__', 'self', 'kw'))}
        kwargs.update(kw)
        super().__init__(**kwargs)


class IPAddressField(RenderMixin, ActionMixin, FieldHelpTextMixin, fields.IPAddressField):

    def __init__(self, protocol='both', read_only=False, write_only=False, required=None, default=fields.empty,
                 initial=fields.empty, source=None, label=None, help_text=None, style=None, error_messages=None,
                 validators=None, allow_null=False, actions: Actions = None, uuid: UUID = None,
                 display: DisplayMode = None, display_table: DisplayMode = None, display_form: DisplayMode = None,
                 table_classes: str = '', **kw):
        kwargs = {k: v for k, v in locals().items() if not k.startswith(('__', 'self', 'kw'))}
        kwargs.update(kw)
        super().__init__(**kwargs)


class IntegerField(RenderMixin, ActionMixin, FieldHelpTextMixin, fields.IntegerField):

    def __init__(self, read_only=False, write_only=False, required=None, default=fields.empty, initial=fields.empty,
                 source=None, label=None, help_text=None, style=None, error_messages=None, validators=None,
                 allow_null=False, actions: Actions = None, uuid: UUID = None, display: DisplayMode = None,
                 display_table: DisplayMode = None, display_form: DisplayMode = None, table_classes: str = '', **kw):
        kwargs = {k: v for k, v in locals().items() if not k.startswith(('__', 'self', 'kw'))}
        kwargs.update(kw)
        super().__init__(**kwargs)


class FloatField(RenderMixin, ActionMixin, FieldHelpTextMixin, fields.FloatField):

    def __init__(self, read_only=False, write_only=False, required=None, default=fields.empty, initial=fields.empty,
                 source=None, label=None, help_text=None, style=None, error_messages=None, validators=None,
                 allow_null=False, actions: Actions = None, uuid: UUID = None, display: DisplayMode = None,
                 display_table: DisplayMode = None, display_form: DisplayMode = None, table_classes: str = '', **kw):
        kwargs = {k: v for k, v in locals().items() if not k.startswith(('__', 'self', 'kw'))}
        kwargs.update(kw)
        super().__init__(**kwargs)


class DecimalField(RenderMixin, ActionMixin, FieldHelpTextMixin, fields.DecimalField):

    def __init__(self, max_digits, decimal_places, coerce_to_string=None, max_value=None, min_value=None,
                 localize=False, rounding=None, read_only=False, write_only=False, required=None, default=fields.empty,
                 initial=fields.empty, source=None, label=None, help_text=None, style=None, error_messages=None,
                 validators=None, allow_null=False, actions: Actions = None, uuid: UUID = None,
                 display: DisplayMode = None, display_table: DisplayMode = None, display_form: DisplayMode = None,
                 table_classes: str = '', **kw):
        kwargs = {k: v for k, v in locals().items() if not k.startswith(('__', 'self', 'kw'))}
        kwargs.update(kw)
        # noinspection PyUnresolvedReferences
        if not version_check(rest_framework.VERSION, '3.7.2'):
            kwargs.pop('rounding', None)
        # noinspection PyUnresolvedReferences
        if not version_check(rest_framework.VERSION, '3.4.0'):
            kwargs.pop('localize', None)
        super().__init__(**kwargs)


# noinspection PyShadowingBuiltins
class DateTimeField(DateTimeFieldMixin, RenderMixin, ActionMixin, FieldHelpTextMixin, fields.DateTimeField):

    def __init__(self, format=fields.empty, input_formats=None, default_timezone=None, read_only=False,
                 write_only=False, required=None, default=fields.empty, initial=fields.empty, source=None, label=None,
                 help_text=None, style=None, error_messages=None, validators=None, allow_null=False,
                 actions: Actions = None, uuid: UUID = None, display: DisplayMode = None,
                 display_table: DisplayMode = None, display_form: DisplayMode = None, table_classes: str = '', **kw):
        kwargs = {k: v for k, v in locals().items() if not k.startswith(('__', 'self', 'kw'))}
        kwargs.update(kw)
        super().__init__(**kwargs)


# noinspection PyShadowingBuiltins
class DateField(DateFieldMixin, RenderMixin, ActionMixin, FieldHelpTextMixin, fields.DateField):

    def __init__(self, format=fields.empty, input_formats=None, read_only=False, write_only=False, required=None,
                 default=fields.empty, initial=fields.empty, source=None, label=None, help_text=None, style=None,
                 error_messages=None, validators=None, allow_null=False, actions: Actions = None, uuid: UUID = None,
                 display: DisplayMode = None, display_table: DisplayMode = None, display_form: DisplayMode = None,
                 table_classes: str = '', **kw):
        self.time_step = kw.pop('time_step', None)
        kwargs = {k: v for k, v in locals().items() if not k.startswith(('__', 'self', 'kw'))}
        kwargs.update(kw)
        super().__init__(**kwargs)


# noinspection PyShadowingBuiltins
class TimeField(TimeFieldMixin, RenderMixin, ActionMixin, FieldHelpTextMixin, fields.TimeField):

    def __init__(self, format=fields.empty, input_formats=None, read_only=False, write_only=False, required=None,
                 default=fields.empty, initial=fields.empty, source=None, label=None, help_text=None, style=None,
                 error_messages=None, validators=None, allow_null=False, actions: Actions = None, uuid: UUID = None,
                 display: DisplayMode = None, display_table: DisplayMode = None, display_form: DisplayMode = None,
                 table_classes: str = '', **kw):
        self.time_step = kw.pop('time_step', None)
        kwargs = {k: v for k, v in locals().items() if not k.startswith(('__', 'self', 'kw'))}
        kwargs.update(kw)
        super().__init__(**kwargs)


class DurationField(RenderMixin, ActionMixin, FieldHelpTextMixin, fields.DurationField):

    def __init__(self, read_only=False, write_only=False, required=None, default=fields.empty, initial=fields.empty,
                 source=None, label=None, help_text=None, style=None, error_messages=None, validators=None,
                 allow_null=False, actions: Actions = None, uuid: UUID = None, display: DisplayMode = None,
                 display_table: DisplayMode = None, display_form: DisplayMode = None, table_classes: str = '', **kw):
        kwargs = {k: v for k, v in locals().items() if not k.startswith(('__', 'self', 'kw'))}
        kwargs.update(kw)
        super().__init__(**kwargs)


class ChoiceField(AllowTagsMixin, NullChoiceMixin, RenderMixin, ActionMixin, FieldHelpTextMixin, fields.ChoiceField):

    def __init__(self, choices, read_only=False, write_only=False, required=None, default=fields.empty,
                 initial=fields.empty, source=None, label=None, help_text=None, style=None, error_messages=None,
                 validators=None, allow_null=False, allow_tags=False, actions: Actions = None, uuid: UUID = None,
                 display: DisplayMode = None, display_table: DisplayMode = None, display_form: DisplayMode = None,
                 table_classes: str = '', **kw):
        kwargs = {k: v for k, v in locals().items() if not k.startswith(('__', 'self', 'kw'))}
        kwargs.update(kw)
        super().__init__(**kwargs)


class MultipleChoiceField(AllowTagsMixin, NullChoiceMixin, RenderMixin, ActionMixin, FieldHelpTextMixin,
                          fields.MultipleChoiceField):
    def __init__(self, choices, read_only=False, write_only=False, required=None, default=fields.empty,
                 initial=fields.empty, source=None, label=None, help_text=None, style=None, error_messages=None,
                 validators=None, allow_null=False, allow_tags=False, actions: Actions = None, uuid: UUID = None,
                 display: DisplayMode = None, display_table: DisplayMode = None, display_form: DisplayMode = None,
                 table_classes: str = '', **kw):
        kwargs = {k: v for k, v in locals().items() if not k.startswith(('__', 'self', 'kw'))}
        kwargs.update(kw)
        super().__init__(**kwargs)


class FilePathField(AllowTagsMixin, NullChoiceMixin, RenderMixin, ActionMixin, FieldHelpTextMixin,
                    fields.FilePathField):
    def __init__(self, path, match=None, recursive=False, allow_files=True, allow_folders=False, required=None,
                 read_only=False, write_only=False, default=fields.empty, initial=fields.empty, source=None,
                 label=None, help_text=None, style=None, error_messages=None, validators=None, allow_null=False,
                 allow_tags=False, actions: Actions = None, uuid: UUID = None, display: DisplayMode = None,
                 display_table: DisplayMode = None, display_form: DisplayMode = None, table_classes: str = '', **kw):
        kwargs = {k: v for k, v in locals().items() if not k.startswith(('__', 'self', 'kw'))}
        kwargs.update(kw)
        super().__init__(**kwargs)


class FileField(RenderMixin, ActionMixin, FieldHelpTextMixin, fields.FileField):

    def __init__(self, read_only=False, write_only=False, required=None, default=fields.empty, initial=fields.empty,
                 source=None, label=None, help_text=None, style=None, error_messages=None, validators=None,
                 allow_null=False, actions: Actions = None, uuid: UUID = None, display: DisplayMode = None,
                 display_table: DisplayMode = None, display_form: DisplayMode = None, table_classes: str = '', **kw):
        kwargs = {k: v for k, v in locals().items() if not k.startswith(('__', 'self', 'kw'))}
        kwargs.update(kw)
        super().__init__(**kwargs)


class ImageField(RenderMixin, ActionMixin, FieldHelpTextMixin, fields.ImageField):

    def __init__(self, read_only=False, write_only=False, required=None, default=fields.empty, initial=fields.empty,
                 source=None, label=None, help_text=None, style=None, error_messages=None, validators=None,
                 allow_null=False, actions: Actions = None, uuid: UUID = None, display: DisplayMode = None,
                 display_table: DisplayMode = None, display_form: DisplayMode = None, table_classes: str = '', **kw):
        kwargs = {k: v for k, v in locals().items() if not k.startswith(('__', 'self', 'kw'))}
        kwargs.update(kw)
        super().__init__(**kwargs)


class ListField(RenderMixin, ActionMixin, FieldHelpTextMixin, fields.ListField):

    def __init__(self, read_only=False, write_only=False, required=None, default=fields.empty, initial=fields.empty,
                 source=None, label=None, help_text=None, style=None, error_messages=None, validators=None,
                 allow_null=False, actions: Actions = None, uuid: UUID = None, display: DisplayMode = None,
                 display_table: DisplayMode = None, display_form: DisplayMode = None, table_classes: str = '', **kw):
        kwargs = {k: v for k, v in locals().items() if not k.startswith(('__', 'self', 'kw'))}
        kwargs.update(kw)
        super().__init__(**kwargs)


class DictField(RenderMixin, ActionMixin, FieldHelpTextMixin, fields.DictField):

    def __init__(self, read_only=False, write_only=False, required=None, default=fields.empty, initial=fields.empty,
                 source=None, label=None, help_text=None, style=None, error_messages=None, validators=None,
                 allow_null=False, actions: Actions = None, uuid: UUID = None, display: DisplayMode = None,
                 display_table: DisplayMode = None, display_form: DisplayMode = None, table_classes: str = '', **kw):
        kwargs = {k: v for k, v in locals().items() if not k.startswith(('__', 'self', 'kw'))}
        kwargs.update(kw)
        super().__init__(**kwargs)


if hasattr(fields, 'HStoreField'):
    class HStoreField(RenderMixin, ActionMixin, FieldHelpTextMixin, fields.HStoreField):

        def __init__(self, read_only=False, write_only=False, required=None, default=fields.empty,
                     initial=fields.empty, source=None, label=None, help_text=None, style=None, error_messages=None,
                     validators=None, allow_null=False, actions: Actions = None, uuid: UUID = None,
                     display: DisplayMode = None, display_table: DisplayMode = None, display_form: DisplayMode = None,
                     table_classes: str = '', **kw):
            kwargs = {k: v for k, v in locals().items() if not k.startswith(('__', 'self', 'kw'))}
            kwargs.update(kw)
            super().__init__(**kwargs)


class JSONField(RenderMixin, ActionMixin, FieldHelpTextMixin, fields.JSONField):

    def __init__(self, read_only=False, write_only=False, required=None, default=fields.empty, initial=fields.empty,
                 source=None, label=None, help_text=None, style=None, error_messages=None, validators=None,
                 allow_null=False, actions: Actions = None, uuid: UUID = None, display: DisplayMode = None,
                 display_table: DisplayMode = None, display_form: DisplayMode = None, table_classes: str = '', **kw):
        kwargs = {k: v for k, v in locals().items() if not k.startswith(('__', 'self', 'kw'))}
        kwargs.update(kw)
        super().__init__(**kwargs)


# noinspection PyAbstractClass
class ReadOnlyField(RenderMixin, ActionMixin, FieldHelpTextMixin, fields.ReadOnlyField):

    def __init__(self, read_only=False, write_only=False, required=None, default=fields.empty, initial=fields.empty,
                 source=None, label=None, help_text=None, style=None, error_messages=None, validators=None,
                 allow_null=False, actions: Actions = None, uuid: UUID = None, display: DisplayMode = None,
                 display_table: DisplayMode = None, display_form: DisplayMode = None, table_classes: str = '', **kw):
        warnings.warn('deprecated - wrong approach! Use read_only attribute instead.',
                      DeprecationWarning, stacklevel=2)
        read_only = True  # NOQA
        kwargs = {k: v for k, v in locals().items() if not k.startswith(('__', 'self', 'kw'))}
        kwargs.update(kw)
        super().__init__(**kwargs)


# noinspection PyAbstractClass
class HiddenField(HiddenFieldMixin, RenderMixin, ActionMixin, FieldHelpTextMixin, fields.HiddenField):

    def __init__(self, read_only=False, write_only=False, required=None, default=fields.empty, initial=fields.empty,
                 source=None, label=None, help_text=None, style=None, error_messages=None, validators=None,
                 allow_null=False, actions: Actions = None, uuid: UUID = None, display: DisplayMode = None,
                 display_table: DisplayMode = None, display_form: DisplayMode = None, table_classes: str = '', **kw):
        warnings.warn('deprecated - wrong approach! Use display(|_table|_form) attributes instead.',
                      DeprecationWarning, stacklevel=2)
        display = DisplayMode.HIDDEN  # NOQA
        kwargs = {k: v for k, v in locals().items() if not k.startswith(('__', 'self', 'kw'))}
        kwargs.update(kw)
        super().__init__(**kwargs)


# noinspection PyAbstractClass
class SerializerMethodField(RenderMixin, ActionMixin, FieldHelpTextMixin, fields.SerializerMethodField):

    def __init__(self, method_name=None, read_only=False, write_only=False, required=None, default=fields.empty,
                 initial=fields.empty, source=None, label=None, help_text=None, style=None, error_messages=None,
                 validators=None, allow_null=False, actions: Actions = None, uuid: UUID = None,
                 display: DisplayMode = None, display_table: DisplayMode = None, display_form: DisplayMode = None,
                 table_classes: str = '', **kw):
        kwargs = {k: v for k, v in locals().items() if not k.startswith(('__', 'self', 'kw'))}
        kwargs.update(kw)
        super().__init__(**kwargs)


class ModelField(RenderMixin, ActionMixin, FieldHelpTextMixin, fields.ModelField):

    def __init__(self, model_field, read_only=False, write_only=False, required=None, default=fields.empty,
                 initial=fields.empty, source=None, label=None, help_text=None, style=None, error_messages=None,
                 validators=None, allow_null=False, actions: Actions = None, uuid: UUID = None,
                 display: DisplayMode = None, display_table: DisplayMode = None, display_form: DisplayMode = None,
                 table_classes: str = '', **kw):
        kwargs = {k: v for k, v in locals().items() if not k.startswith(('__', 'self', 'kw'))}
        kwargs.update(kw)
        super().__init__(**kwargs)


class StringRelatedField(RelatedFieldAJAXMixin, RenderMixin, ActionMixin, FieldHelpTextMixin,
                         relations.StringRelatedField):
    def __init__(self, read_only=False, write_only=False, required=None, default=fields.empty, initial=fields.empty,
                 source=None, label=None, help_text=None, style=None, error_messages=None, validators=None,
                 allow_null=False, url_reverse: Optional[str] = None, placeholder: Optional[str] = None,
                 additional_parameters: Optional[dict] = None, query_field: str = 'query', actions: Actions = None,
                 uuid: UUID = None, display: DisplayMode = None, display_table: DisplayMode = None,
                 display_form: DisplayMode = None, table_classes: str = '', **kw):
        kwargs = {k: v for k, v in locals().items() if not k.startswith(('__', 'self', 'kw'))}
        kwargs.update(kw)
        super().__init__(**kwargs)


class PrimaryKeyRelatedField(RelatedFieldAJAXMixin, RenderMixin, ActionMixin, FieldHelpTextMixin,
                             relations.PrimaryKeyRelatedField):
    def __init__(self, read_only=False, write_only=False, required=None, default=fields.empty, initial=fields.empty,
                 source=None, label=None, help_text=None, style=None, error_messages=None, validators=None,
                 allow_null=False, url_reverse: Optional[str] = None, placeholder: Optional[str] = None,
                 additional_parameters: Optional[dict] = None, query_field: str = 'query', actions: Actions = None,
                 uuid: UUID = None, display: DisplayMode = None, display_table: DisplayMode = None,
                 display_form: DisplayMode = None, table_classes: str = '', **kw):
        kwargs = {k: v for k, v in locals().items() if not k.startswith(('__', 'self', 'kw'))}
        kwargs.update(kw)
        super().__init__(**kwargs)


class HyperlinkedRelatedField(RelatedFieldAJAXMixin, RenderMixin, ActionMixin, FieldHelpTextMixin,
                              relations.HyperlinkedRelatedField):
    def __init__(self, view_name=None, read_only=False, write_only=False, required=None, default=fields.empty,
                 initial=fields.empty, source=None, label=None, help_text=None, style=None, error_messages=None,
                 validators=None, allow_null=False, url_reverse: Optional[str] = None,
                 placeholder: Optional[str] = None, additional_parameters: Optional[dict] = None,
                 query_field: str = 'query', actions: Actions = None, uuid: UUID = None, display: DisplayMode = None,
                 display_table: DisplayMode = None, display_form: DisplayMode = None, table_classes: str = '', **kw):
        kwargs = {k: v for k, v in locals().items() if not k.startswith(('__', 'self', 'kw'))}
        kwargs.update(kw)
        super().__init__(**kwargs)


class HyperlinkedIdentityField(RelatedFieldAJAXMixin, RenderMixin, ActionMixin, FieldHelpTextMixin,
                               relations.HyperlinkedIdentityField):
    def __init__(self, view_name=None, read_only=False, write_only=False, required=None, default=fields.empty,
                 initial=fields.empty, source=None, label=None, help_text=None, style=None, error_messages=None,
                 validators=None, allow_null=False, url_reverse: Optional[str] = None,
                 placeholder: Optional[str] = None, additional_parameters: Optional[dict] = None,
                 query_field: str = 'query', actions: Actions = None, uuid: UUID = None, display: DisplayMode = None,
                 display_table: DisplayMode = None, display_form: DisplayMode = None, table_classes: str = '', **kw):
        kwargs = {k: v for k, v in locals().items() if not k.startswith(('__', 'self', 'kw'))}
        kwargs.update(kw)
        super().__init__(**kwargs)


class SlugRelatedField(RelatedFieldAJAXMixin, RenderMixin, ActionMixin, FieldHelpTextMixin, relations.SlugRelatedField):

    def __init__(self, slug_field=None, read_only=False, write_only=False, required=None, default=fields.empty,
                 initial=fields.empty, source=None, label=None, help_text=None, style=None, error_messages=None,
                 validators=None, allow_null=False, url_reverse: Optional[str] = None,
                 placeholder: Optional[str] = None, additional_parameters: Optional[dict] = None,
                 query_field: str = 'query', actions: Actions = None, uuid: UUID = None, display: DisplayMode = None,
                 display_table: DisplayMode = None, display_form: DisplayMode = None, table_classes: str = '', **kw):
        kwargs = {k: v for k, v in locals().items() if not k.startswith(('__', 'self', 'kw'))}
        kwargs.update(kw)
        super().__init__(**kwargs)


class ManyRelatedField(RelatedFieldAJAXMixin, RenderMixin, ActionMixin, FieldHelpTextMixin, relations.ManyRelatedField):

    def __init__(self, child_relation=None, read_only=False, write_only=False, required=None, default=fields.empty,
                 initial=fields.empty, source=None, label=None, help_text=None, style=None, error_messages=None,
                 validators=None, allow_null=True, actions: Actions = None, uuid: UUID = None,
                 display: DisplayMode = None, display_table: DisplayMode = None, display_form: DisplayMode = None,
                 table_classes: str = '', **kw):
        kwargs = {k: v for k, v in locals().items() if not k.startswith(('__', 'self', 'kw'))}
        kwargs.update(kw)
        super().__init__(**kwargs)
