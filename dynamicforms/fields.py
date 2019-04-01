from typing import Optional
from uuid import UUID

import rest_framework
from rest_framework import fields, relations

from .action import Actions
from .mixins import ActionMixin, DateFieldMixin, DateTimeFieldMixin, HiddenFieldMixin, NullChoiceMixin, \
    RelatedFieldAJAXMixin, RenderToTableMixin, TimeFieldMixin, UUIDMixIn
from .settings import version_check


class BooleanField(UUIDMixIn, ActionMixin, RenderToTableMixin, fields.BooleanField):

    def __init__(self, read_only=False, write_only=False, required=None, default=fields.empty, initial=fields.empty,
                 source=None, label=None, help_text=None, style=None, error_messages=None, validators=None,
                 actions: Actions = None, visible_in_table: bool = True, table_classes: str = '', uuid: UUID = None,
                 **kw):
        kwargs = {k: v for k, v in locals().items() if not k.startswith(('__', 'self', 'kw'))}
        kwargs.update(kw)
        super().__init__(**kwargs)


class NullBooleanField(UUIDMixIn, ActionMixin, RenderToTableMixin, fields.NullBooleanField):

    def __init__(self, read_only=False, write_only=False, required=None, default=fields.empty, initial=fields.empty,
                 source=None, label=None, help_text=None, style=None, error_messages=None, validators=None,
                 actions: Actions = None, visible_in_table: bool = True, table_classes: str = '', uuid: UUID = None,
                 **kw):
        kwargs = {k: v for k, v in locals().items() if not k.startswith(('__', 'self', 'kw'))}
        kwargs.update(kw)
        super().__init__(**kwargs)


class CharField(UUIDMixIn, ActionMixin, RenderToTableMixin, fields.CharField):

    def __init__(self, read_only=False, write_only=False, required=None, default=fields.empty, initial=fields.empty,
                 source=None, label=None, help_text=None, style=None, error_messages=None, validators=None,
                 allow_null=False, actions: Actions = None, visible_in_table: bool = True, table_classes: str = '',
                 uuid: UUID = None, **kw):
        kwargs = {k: v for k, v in locals().items() if not k.startswith(('__', 'self', 'kw'))}
        kwargs.update(kw)
        super().__init__(**kwargs)


class EmailField(UUIDMixIn, ActionMixin, RenderToTableMixin, fields.EmailField):

    def __init__(self, read_only=False, write_only=False, required=None, default=fields.empty, initial=fields.empty,
                 source=None, label=None, help_text=None, style=None, error_messages=None, validators=None,
                 allow_null=False, actions: Actions = None, visible_in_table: bool = True, table_classes: str = '',
                 uuid: UUID = None, **kw):
        kwargs = {k: v for k, v in locals().items() if not k.startswith(('__', 'self', 'kw'))}
        kwargs.update(kw)
        super().__init__(**kwargs)


class RegexField(UUIDMixIn, ActionMixin, RenderToTableMixin, fields.RegexField):

    def __init__(self, regex, read_only=False, write_only=False, required=None, default=fields.empty,
                 initial=fields.empty, source=None, label=None, help_text=None, style=None, error_messages=None,
                 validators=None, allow_null=False, actions: Actions = None, visible_in_table: bool = True,
                 table_classes: str = '', uuid: UUID = None, **kw):
        kwargs = {k: v for k, v in locals().items() if not k.startswith(('__', 'self', 'kw'))}
        kwargs.update(kw)
        super().__init__(**kwargs)


class SlugField(UUIDMixIn, ActionMixin, RenderToTableMixin, fields.SlugField):

    def __init__(self, allow_unicode=False, read_only=False, write_only=False, required=None, default=fields.empty,
                 initial=fields.empty, source=None, label=None, help_text=None, style=None, error_messages=None,
                 validators=None, allow_null=False, actions: Actions = None, visible_in_table: bool = True,
                 table_classes: str = '', uuid: UUID = None, **kw):
        kwargs = {k: v for k, v in locals().items() if not k.startswith(('__', 'self', 'kw'))}
        kwargs.update(kw)
        # noinspection PyUnresolvedReferences
        if not version_check(rest_framework.VERSION, '3.6.4'):
            kwargs.pop('allow_unicode', None)
        super().__init__(**kwargs)


class URLField(UUIDMixIn, ActionMixin, RenderToTableMixin, fields.URLField):

    def __init__(self, read_only=False, write_only=False, required=None, default=fields.empty, initial=fields.empty,
                 source=None, label=None, help_text=None, style=None, error_messages=None, validators=None,
                 allow_null=False, actions: Actions = None, visible_in_table: bool = True, table_classes: str = '',
                 uuid: UUID = None, **kw):
        kwargs = {k: v for k, v in locals().items() if not k.startswith(('__', 'self', 'kw'))}
        kwargs.update(kw)
        super().__init__(**kwargs)


class UUIDField(UUIDMixIn, ActionMixin, RenderToTableMixin, fields.UUIDField):

    def __init__(self, read_only=False, write_only=False, required=None, default=fields.empty, initial=fields.empty,
                 source=None, label=None, help_text=None, style=None, error_messages=None, validators=None,
                 allow_null=False, actions: Actions = None, visible_in_table: bool = True, table_classes: str = '',
                 uuid: UUID = None, **kw):
        kwargs = {k: v for k, v in locals().items() if not k.startswith(('__', 'self', 'kw'))}
        kwargs.update(kw)
        super().__init__(**kwargs)


class IPAddressField(UUIDMixIn, ActionMixin, RenderToTableMixin, fields.IPAddressField):

    def __init__(self, protocol='both', read_only=False, write_only=False, required=None, default=fields.empty,
                 initial=fields.empty, source=None, label=None, help_text=None, style=None, error_messages=None,
                 validators=None, allow_null=False, actions: Actions = None, visible_in_table: bool = True,
                 table_classes: str = '', uuid: UUID = None, **kw):
        kwargs = {k: v for k, v in locals().items() if not k.startswith(('__', 'self', 'kw'))}
        kwargs.update(kw)
        super().__init__(**kwargs)


class IntegerField(UUIDMixIn, ActionMixin, RenderToTableMixin, fields.IntegerField):

    def __init__(self, read_only=False, write_only=False, required=None, default=fields.empty, initial=fields.empty,
                 source=None, label=None, help_text=None, style=None, error_messages=None, validators=None,
                 allow_null=False, actions: Actions = None, visible_in_table: bool = True, table_classes: str = '',
                 uuid: UUID = None, **kw):
        kwargs = {k: v for k, v in locals().items() if not k.startswith(('__', 'self', 'kw'))}
        kwargs.update(kw)
        super().__init__(**kwargs)


class FloatField(UUIDMixIn, ActionMixin, RenderToTableMixin, fields.FloatField):

    def __init__(self, read_only=False, write_only=False, required=None, default=fields.empty, initial=fields.empty,
                 source=None, label=None, help_text=None, style=None, error_messages=None, validators=None,
                 allow_null=False, actions: Actions = None, visible_in_table: bool = True, table_classes: str = '',
                 uuid: UUID = None, **kw):
        kwargs = {k: v for k, v in locals().items() if not k.startswith(('__', 'self', 'kw'))}
        kwargs.update(kw)
        super().__init__(**kwargs)


class DecimalField(UUIDMixIn, ActionMixin, RenderToTableMixin, fields.DecimalField):

    def __init__(self, max_digits, decimal_places, coerce_to_string=None, max_value=None, min_value=None,
                 localize=False, rounding=None, read_only=False, write_only=False, required=None, default=fields.empty,
                 initial=fields.empty, source=None, label=None, help_text=None, style=None, error_messages=None,
                 validators=None, allow_null=False, actions: Actions = None, visible_in_table: bool = True,
                 table_classes: str = '', uuid: UUID = None, **kw):
        kwargs = {k: v for k, v in locals().items() if not k.startswith(('__', 'self', 'kw'))}
        kwargs.update(kw)
        # noinspection PyUnresolvedReferences
        if not version_check(rest_framework.VERSION, '3.7.2'):
            kwargs.pop('rounding', None)
        if not version_check(rest_framework.VERSION, '3.4.0'):
            kwargs.pop('localize', None)
        super().__init__(**kwargs)


# noinspection PyShadowingBuiltins
class DateTimeField(DateTimeFieldMixin, UUIDMixIn, ActionMixin, RenderToTableMixin, fields.DateTimeField):

    def __init__(self, format=fields.empty, input_formats=None, default_timezone=None, read_only=False,
                 write_only=False, required=None, default=fields.empty, initial=fields.empty, source=None, label=None,
                 help_text=None, style=None, error_messages=None, validators=None, allow_null=False, actions: Actions =
                 None, visible_in_table: bool = True, table_classes: str = '', uuid: UUID = None, **kw):
        kwargs = {k: v for k, v in locals().items() if not k.startswith(('__', 'self', 'kw'))}
        kwargs.update(kw)
        super().__init__(**kwargs)


# noinspection PyShadowingBuiltins
class DateField(DateFieldMixin, UUIDMixIn, ActionMixin, RenderToTableMixin, fields.DateField):

    def __init__(self, format=fields.empty, input_formats=None, read_only=False, write_only=False, required=None,
                 default=fields.empty, initial=fields.empty, source=None, label=None, help_text=None, style=None,
                 error_messages=None, validators=None, allow_null=False, actions: Actions = None, visible_in_table: bool
                 = True, table_classes: str = '', uuid: UUID = None, **kw):
        kwargs = {k: v for k, v in locals().items() if not k.startswith(('__', 'self', 'kw'))}
        kwargs.update(kw)
        super().__init__(**kwargs)


# noinspection PyShadowingBuiltins
class TimeField(TimeFieldMixin, UUIDMixIn, ActionMixin, RenderToTableMixin, fields.TimeField):

    def __init__(self, format=fields.empty, input_formats=None, read_only=False, write_only=False, required=None,
                 default=fields.empty, initial=fields.empty, source=None, label=None, help_text=None, style=None,
                 error_messages=None, validators=None, allow_null=False, actions: Actions = None, visible_in_table: bool
                 = True, table_classes: str = '', uuid: UUID = None, **kw):
        kwargs = {k: v for k, v in locals().items() if not k.startswith(('__', 'self', 'kw'))}
        kwargs.update(kw)
        super().__init__(**kwargs)


class DurationField(UUIDMixIn, ActionMixin, RenderToTableMixin, fields.DurationField):

    def __init__(self, read_only=False, write_only=False, required=None, default=fields.empty, initial=fields.empty,
                 source=None, label=None, help_text=None, style=None, error_messages=None, validators=None,
                 allow_null=False, actions: Actions = None, visible_in_table: bool = True, table_classes: str = '',
                 uuid: UUID = None, **kw):
        kwargs = {k: v for k, v in locals().items() if not k.startswith(('__', 'self', 'kw'))}
        kwargs.update(kw)
        super().__init__(**kwargs)


class ChoiceField(NullChoiceMixin, UUIDMixIn, ActionMixin, RenderToTableMixin, fields.ChoiceField):

    def __init__(self, choices, read_only=False, write_only=False, required=None, default=fields.empty,
                 initial=fields.empty, source=None, label=None, help_text=None, style=None, error_messages=None,
                 validators=None, allow_null=False, actions: Actions = None, visible_in_table: bool = True,
                 table_classes: str = '', uuid: UUID = None, **kw):
        kwargs = {k: v for k, v in locals().items() if not k.startswith(('__', 'self', 'kw'))}
        kwargs.update(kw)
        super().__init__(**kwargs)


class MultipleChoiceField(NullChoiceMixin, UUIDMixIn, ActionMixin, RenderToTableMixin, fields.MultipleChoiceField):

    def __init__(self, choices, read_only=False, write_only=False, required=None, default=fields.empty,
                 initial=fields.empty, source=None, label=None, help_text=None, style=None, error_messages=None,
                 validators=None, allow_null=False, actions: Actions = None, visible_in_table: bool = True,
                 table_classes: str = '', uuid: UUID = None, **kw):
        kwargs = {k: v for k, v in locals().items() if not k.startswith(('__', 'self', 'kw'))}
        kwargs.update(kw)
        super().__init__(**kwargs)


class FilePathField(NullChoiceMixin, UUIDMixIn, ActionMixin, RenderToTableMixin, fields.FilePathField):

    def __init__(self, path, match=None, recursive=False, allow_files=True, allow_folders=False, required=None,
                 read_only=False, write_only=False, default=fields.empty, initial=fields.empty, source=None, label=None,
                 help_text=None, style=None, error_messages=None, validators=None, allow_null=False, actions: Actions =
                 None, visible_in_table: bool = True, table_classes: str = '', uuid: UUID = None, **kw):
        kwargs = {k: v for k, v in locals().items() if not k.startswith(('__', 'self', 'kw'))}
        kwargs.update(kw)
        super().__init__(**kwargs)


class FileField(UUIDMixIn, ActionMixin, RenderToTableMixin, fields.FileField):

    def __init__(self, read_only=False, write_only=False, required=None, default=fields.empty, initial=fields.empty,
                 source=None, label=None, help_text=None, style=None, error_messages=None, validators=None,
                 allow_null=False, actions: Actions = None, visible_in_table: bool = True, table_classes: str = '',
                 uuid: UUID = None, **kw):
        kwargs = {k: v for k, v in locals().items() if not k.startswith(('__', 'self', 'kw'))}
        kwargs.update(kw)
        super().__init__(**kwargs)


class ImageField(UUIDMixIn, ActionMixin, RenderToTableMixin, fields.ImageField):

    def __init__(self, read_only=False, write_only=False, required=None, default=fields.empty, initial=fields.empty,
                 source=None, label=None, help_text=None, style=None, error_messages=None, validators=None,
                 allow_null=False, actions: Actions = None, visible_in_table: bool = True, table_classes: str = '',
                 uuid: UUID = None, **kw):
        kwargs = {k: v for k, v in locals().items() if not k.startswith(('__', 'self', 'kw'))}
        kwargs.update(kw)
        super().__init__(**kwargs)


class ListField(UUIDMixIn, ActionMixin, RenderToTableMixin, fields.ListField):

    def __init__(self, read_only=False, write_only=False, required=None, default=fields.empty, initial=fields.empty,
                 source=None, label=None, help_text=None, style=None, error_messages=None, validators=None,
                 allow_null=False, actions: Actions = None, visible_in_table: bool = True, table_classes: str = '',
                 uuid: UUID = None, **kw):
        kwargs = {k: v for k, v in locals().items() if not k.startswith(('__', 'self', 'kw'))}
        kwargs.update(kw)
        super().__init__(**kwargs)


class DictField(UUIDMixIn, ActionMixin, RenderToTableMixin, fields.DictField):

    def __init__(self, read_only=False, write_only=False, required=None, default=fields.empty, initial=fields.empty,
                 source=None, label=None, help_text=None, style=None, error_messages=None, validators=None,
                 allow_null=False, actions: Actions = None, visible_in_table: bool = True, table_classes: str = '',
                 uuid: UUID = None, **kw):
        kwargs = {k: v for k, v in locals().items() if not k.startswith(('__', 'self', 'kw'))}
        kwargs.update(kw)
        super().__init__(**kwargs)


if hasattr(fields, 'HStoreField'):
    class HStoreField(UUIDMixIn, ActionMixin, RenderToTableMixin, fields.HStoreField):

        def __init__(self, read_only=False, write_only=False, required=None, default=fields.empty, initial=fields.empty,
                     source=None, label=None, help_text=None, style=None, error_messages=None, validators=None,
                     allow_null=False, actions: Actions = None, visible_in_table: bool = True, table_classes: str = '',
                     uuid: UUID = None, **kw):
            kwargs = {k: v for k, v in locals().items() if not k.startswith(('__', 'self', 'kw'))}
            kwargs.update(kw)
            super().__init__(**kwargs)


class JSONField(UUIDMixIn, ActionMixin, RenderToTableMixin, fields.JSONField):

    def __init__(self, read_only=False, write_only=False, required=None, default=fields.empty, initial=fields.empty,
                 source=None, label=None, help_text=None, style=None, error_messages=None, validators=None,
                 allow_null=False, actions: Actions = None, visible_in_table: bool = True, table_classes: str = '',
                 uuid: UUID = None, **kw):
        kwargs = {k: v for k, v in locals().items() if not k.startswith(('__', 'self', 'kw'))}
        kwargs.update(kw)
        super().__init__(**kwargs)


# noinspection PyAbstractClass
class ReadOnlyField(UUIDMixIn, ActionMixin, RenderToTableMixin, fields.ReadOnlyField):

    def __init__(self, read_only=False, write_only=False, required=None, default=fields.empty, initial=fields.empty,
                 source=None, label=None, help_text=None, style=None, error_messages=None, validators=None,
                 allow_null=False, actions: Actions = None, visible_in_table: bool = True, table_classes: str = '',
                 uuid: UUID = None, **kw):
        kwargs = {k: v for k, v in locals().items() if not k.startswith(('__', 'self', 'kw'))}
        kwargs.update(kw)
        super().__init__(**kwargs)


# noinspection PyAbstractClass
class HiddenField(HiddenFieldMixin, UUIDMixIn, ActionMixin, RenderToTableMixin, fields.HiddenField):

    def __init__(self, read_only=False, write_only=False, required=None, default=fields.empty, initial=fields.empty,
                 source=None, label=None, help_text=None, style=None, error_messages=None, validators=None,
                 allow_null=False, actions: Actions = None, visible_in_table: bool = True, table_classes: str = '',
                 uuid: UUID = None, **kw):
        kwargs = {k: v for k, v in locals().items() if not k.startswith(('__', 'self', 'kw'))}
        kwargs.update(kw)
        super().__init__(**kwargs)


# noinspection PyAbstractClass
class SerializerMethodField(UUIDMixIn, ActionMixin, RenderToTableMixin, fields.SerializerMethodField):

    def __init__(self, method_name=None, read_only=False, write_only=False, required=None, default=fields.empty,
                 initial=fields.empty, source=None, label=None, help_text=None, style=None, error_messages=None,
                 validators=None, allow_null=False, actions: Actions = None, visible_in_table: bool = True,
                 table_classes: str = '', uuid: UUID = None, **kw):
        kwargs = {k: v for k, v in locals().items() if not k.startswith(('__', 'self', 'kw'))}
        kwargs.update(kw)
        super().__init__(**kwargs)


class ModelField(UUIDMixIn, ActionMixin, RenderToTableMixin, fields.ModelField):

    def __init__(self, model_field, read_only=False, write_only=False, required=None, default=fields.empty,
                 initial=fields.empty, source=None, label=None, help_text=None, style=None, error_messages=None,
                 validators=None, allow_null=False, actions: Actions = None, visible_in_table: bool = True,
                 table_classes: str = '', uuid: UUID = None, **kw):
        kwargs = {k: v for k, v in locals().items() if not k.startswith(('__', 'self', 'kw'))}
        kwargs.update(kw)
        super().__init__(**kwargs)


class StringRelatedField(RelatedFieldAJAXMixin, UUIDMixIn, ActionMixin, RenderToTableMixin,
                         relations.StringRelatedField):
    def __init__(self, read_only=False, write_only=False, required=None, default=fields.empty, initial=fields.empty,
                 source=None, label=None, help_text=None, style=None, error_messages=None, validators=None,
                 allow_null=False, url_reverse: Optional[str] = None, placeholder: Optional[str] = None,
                 additional_parameters: Optional[dict] = None, query_field: str = 'query', actions: Actions = None,
                 visible_in_table: bool = True, table_classes: str = '', uuid: UUID = None, **kw):
        kwargs = {k: v for k, v in locals().items() if not k.startswith(('__', 'self', 'kw'))}
        kwargs.update(kw)
        super().__init__(**kwargs)


class PrimaryKeyRelatedField(RelatedFieldAJAXMixin, UUIDMixIn, ActionMixin, RenderToTableMixin,
                             relations.PrimaryKeyRelatedField):
    def __init__(self, read_only=False, write_only=False, required=None, default=fields.empty, initial=fields.empty,
                 source=None, label=None, help_text=None, style=None, error_messages=None, validators=None,
                 allow_null=False, url_reverse: Optional[str] = None, placeholder: Optional[str] = None,
                 additional_parameters: Optional[dict] = None, query_field: str = 'query', actions: Actions = None,
                 visible_in_table: bool = True, table_classes: str = '', uuid: UUID = None, **kw):
        kwargs = {k: v for k, v in locals().items() if not k.startswith(('__', 'self', 'kw'))}
        kwargs.update(kw)
        super().__init__(**kwargs)


class HyperlinkedRelatedField(RelatedFieldAJAXMixin, UUIDMixIn, ActionMixin, RenderToTableMixin,
                              relations.HyperlinkedRelatedField):
    def __init__(self, view_name=None, read_only=False, write_only=False, required=None, default=fields.empty,
                 initial=fields.empty, source=None, label=None, help_text=None, style=None, error_messages=None,
                 validators=None, allow_null=False, url_reverse: Optional[str] = None, placeholder: Optional[str] =
                 None, additional_parameters: Optional[dict] = None, query_field: str = 'query', actions: Actions =
                 None, visible_in_table: bool = True, table_classes: str = '', uuid: UUID = None, **kw):
        kwargs = {k: v for k, v in locals().items() if not k.startswith(('__', 'self', 'kw'))}
        kwargs.update(kw)
        super().__init__(**kwargs)


class HyperlinkedIdentityField(RelatedFieldAJAXMixin, UUIDMixIn, ActionMixin, RenderToTableMixin,
                               relations.HyperlinkedIdentityField):
    def __init__(self, view_name=None, read_only=False, write_only=False, required=None, default=fields.empty,
                 initial=fields.empty, source=None, label=None, help_text=None, style=None, error_messages=None,
                 validators=None, allow_null=False, url_reverse: Optional[str] = None, placeholder: Optional[str] =
                 None, additional_parameters: Optional[dict] = None, query_field: str = 'query', actions: Actions =
                 None, visible_in_table: bool = True, table_classes: str = '', uuid: UUID = None, **kw):
        kwargs = {k: v for k, v in locals().items() if not k.startswith(('__', 'self', 'kw'))}
        kwargs.update(kw)
        super().__init__(**kwargs)


class SlugRelatedField(RelatedFieldAJAXMixin, UUIDMixIn, ActionMixin, RenderToTableMixin, relations.SlugRelatedField):

    def __init__(self, slug_field=None, read_only=False, write_only=False, required=None, default=fields.empty,
                 initial=fields.empty, source=None, label=None, help_text=None, style=None, error_messages=None,
                 validators=None, allow_null=False, url_reverse: Optional[str] = None, placeholder: Optional[str] =
                 None, additional_parameters: Optional[dict] = None, query_field: str = 'query', actions: Actions =
                 None, visible_in_table: bool = True, table_classes: str = '', uuid: UUID = None, **kw):
        kwargs = {k: v for k, v in locals().items() if not k.startswith(('__', 'self', 'kw'))}
        kwargs.update(kw)
        super().__init__(**kwargs)


class ManyRelatedField(UUIDMixIn, ActionMixin, RenderToTableMixin, relations.ManyRelatedField):

    def __init__(self, child_relation=None, read_only=False, write_only=False, required=None, default=fields.empty,
                 initial=fields.empty, source=None, label=None, help_text=None, style=None, error_messages=None,
                 validators=None, allow_null=True, actions: Actions = None, visible_in_table: bool = True,
                 table_classes: str = '', uuid: UUID = None, **kw):
        kwargs = {k: v for k, v in locals().items() if not k.startswith(('__', 'self', 'kw'))}
        kwargs.update(kw)
        super().__init__(**kwargs)
