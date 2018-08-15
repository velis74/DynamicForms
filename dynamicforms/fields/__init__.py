from uuid import UUID
from .mixins import UUIDMixIn
from rest_framework import fields
from rest_framework.fields import (
    BooleanField, NullBooleanField, CharField, EmailField, RegexField, SlugField, URLField, UUIDField,
    IPAddressField, IntegerField, FloatField, DecimalField, DateTimeField, DateField, TimeField, DurationField,
    ChoiceField, MultipleChoiceField, FilePathField, FileField, ImageField, ListField, DictField, HStoreField,
    JSONField, ReadOnlyField, HiddenField, SerializerMethodField, ModelField
)


# noinspection PyRedeclaration
class BooleanField(UUIDMixIn, BooleanField):

    def __init__(self, read_only=False, write_only=False, required=None, default=fields.empty, initial=fields.empty,
                 source=None, label=None, help_text=None, style=None, error_messages=None, validators=None,
                 uuid: UUID=None, **kw):
        kwargs = {k: v for k, v in locals().items() if not k.startswith(('__', 'self', 'kw'))}
        kwargs.update(kw)
        super().__init__(**kwargs)


# noinspection PyRedeclaration
class NullBooleanField(UUIDMixIn, NullBooleanField):

    def __init__(self, read_only=False, write_only=False, required=None, default=fields.empty, initial=fields.empty,
                 source=None, label=None, help_text=None, style=None, error_messages=None, validators=None,
                 allow_null=False, uuid: UUID=None, **kw):
        kwargs = {k: v for k, v in locals().items() if not k.startswith(('__', 'self', 'kw'))}
        kwargs.update(kw)
        super().__init__(**kwargs)


# noinspection PyRedeclaration
class CharField(UUIDMixIn, CharField):

    def __init__(self, read_only=False, write_only=False, required=None, default=fields.empty, initial=fields.empty,
                 source=None, label=None, help_text=None, style=None, error_messages=None, validators=None,
                 allow_null=False, uuid: UUID=None, **kw):
        kwargs = {k: v for k, v in locals().items() if not k.startswith(('__', 'self', 'kw'))}
        kwargs.update(kw)
        super().__init__(**kwargs)


# noinspection PyRedeclaration
class EmailField(UUIDMixIn, EmailField):

    def __init__(self, read_only=False, write_only=False, required=None, default=fields.empty, initial=fields.empty,
                 source=None, label=None, help_text=None, style=None, error_messages=None, validators=None,
                 allow_null=False, uuid: UUID=None, **kw):
        kwargs = {k: v for k, v in locals().items() if not k.startswith(('__', 'self', 'kw'))}
        kwargs.update(kw)
        super().__init__(**kwargs)


# noinspection PyRedeclaration
class RegexField(UUIDMixIn, RegexField):

    def __init__(self, regex, read_only=False, write_only=False, required=None, default=fields.empty,
                 initial=fields.empty, source=None, label=None, help_text=None, style=None, error_messages=None,
                 validators=None, allow_null=False, uuid: UUID=None, **kw):
        kwargs = {k: v for k, v in locals().items() if not k.startswith(('__', 'self', 'kw'))}
        kwargs.update(kw)
        super().__init__(**kwargs)


# noinspection PyRedeclaration
class SlugField(UUIDMixIn, SlugField):

    def __init__(self, allow_unicode=False, read_only=False, write_only=False, required=None, default=fields.empty,
                 initial=fields.empty, source=None, label=None, help_text=None, style=None, error_messages=None,
                 validators=None, allow_null=False, uuid: UUID=None, **kw):
        kwargs = {k: v for k, v in locals().items() if not k.startswith(('__', 'self', 'kw'))}
        kwargs.update(kw)
        super().__init__(**kwargs)


# noinspection PyRedeclaration
class URLField(UUIDMixIn, URLField):

    def __init__(self, read_only=False, write_only=False, required=None, default=fields.empty, initial=fields.empty,
                 source=None, label=None, help_text=None, style=None, error_messages=None, validators=None,
                 allow_null=False, uuid: UUID=None, **kw):
        kwargs = {k: v for k, v in locals().items() if not k.startswith(('__', 'self', 'kw'))}
        kwargs.update(kw)
        super().__init__(**kwargs)


# noinspection PyRedeclaration
class UUIDField(UUIDMixIn, UUIDField):

    def __init__(self, read_only=False, write_only=False, required=None, default=fields.empty, initial=fields.empty,
                 source=None, label=None, help_text=None, style=None, error_messages=None, validators=None,
                 allow_null=False, uuid: UUID=None, **kw):
        kwargs = {k: v for k, v in locals().items() if not k.startswith(('__', 'self', 'kw'))}
        kwargs.update(kw)
        super().__init__(**kwargs)


# noinspection PyRedeclaration
class IPAddressField(UUIDMixIn, IPAddressField):

    def __init__(self, protocol='both', read_only=False, write_only=False, required=None, default=fields.empty,
                 initial=fields.empty, source=None, label=None, help_text=None, style=None, error_messages=None,
                 validators=None, allow_null=False, uuid: UUID=None, **kw):
        kwargs = {k: v for k, v in locals().items() if not k.startswith(('__', 'self', 'kw'))}
        kwargs.update(kw)
        super().__init__(**kwargs)


# noinspection PyRedeclaration
class IntegerField(UUIDMixIn, IntegerField):

    def __init__(self, read_only=False, write_only=False, required=None, default=fields.empty, initial=fields.empty,
                 source=None, label=None, help_text=None, style=None, error_messages=None, validators=None,
                 allow_null=False, uuid: UUID=None, **kw):
        kwargs = {k: v for k, v in locals().items() if not k.startswith(('__', 'self', 'kw'))}
        kwargs.update(kw)
        super().__init__(**kwargs)


# noinspection PyRedeclaration
class FloatField(UUIDMixIn, FloatField):

    def __init__(self, read_only=False, write_only=False, required=None, default=fields.empty, initial=fields.empty,
                 source=None, label=None, help_text=None, style=None, error_messages=None, validators=None,
                 allow_null=False, uuid: UUID=None, **kw):
        kwargs = {k: v for k, v in locals().items() if not k.startswith(('__', 'self', 'kw'))}
        kwargs.update(kw)
        super().__init__(**kwargs)


# noinspection PyRedeclaration
class DecimalField(UUIDMixIn, DecimalField):

    def __init__(self, max_digits, decimal_places, coerce_to_string=None, max_value=None, min_value=None,
                 localize=False, rounding=None, read_only=False, write_only=False, required=None, default=fields.empty,
                 initial=fields.empty, source=None, label=None, help_text=None, style=None, error_messages=None,
                 validators=None, allow_null=False, uuid: UUID=None, **kw):
        kwargs = {k: v for k, v in locals().items() if not k.startswith(('__', 'self', 'kw'))}
        kwargs.update(kw)
        super().__init__(**kwargs)


# noinspection PyRedeclaration,PyShadowingBuiltins
class DateTimeField(UUIDMixIn, DateTimeField):

    def __init__(self, format=fields.empty, input_formats=None, default_timezone=None, read_only=False,
                 write_only=False, required=None, default=fields.empty, initial=fields.empty, source=None, label=None,
                 help_text=None, style=None, error_messages=None, validators=None, allow_null=False, uuid: UUID=None,
                 **kw):
        kwargs = {k: v for k, v in locals().items() if not k.startswith(('__', 'self', 'kw'))}
        kwargs.update(kw)
        super().__init__(**kwargs)


# noinspection PyRedeclaration,PyShadowingBuiltins
class DateField(UUIDMixIn, DateField):

    def __init__(self, format=fields.empty, input_formats=None, read_only=False, write_only=False, required=None,
                 default=fields.empty, initial=fields.empty, source=None, label=None, help_text=None, style=None,
                 error_messages=None, validators=None, allow_null=False, uuid: UUID=None, **kw):
        kwargs = {k: v for k, v in locals().items() if not k.startswith(('__', 'self', 'kw'))}
        kwargs.update(kw)
        super().__init__(**kwargs)


# noinspection PyRedeclaration,PyShadowingBuiltins
class TimeField(UUIDMixIn, TimeField):

    def __init__(self, format=fields.empty, input_formats=None, read_only=False, write_only=False, required=None,
                 default=fields.empty, initial=fields.empty, source=None, label=None, help_text=None, style=None,
                 error_messages=None, validators=None, allow_null=False, uuid: UUID=None, **kw):
        kwargs = {k: v for k, v in locals().items() if not k.startswith(('__', 'self', 'kw'))}
        kwargs.update(kw)
        super().__init__(**kwargs)


# noinspection PyRedeclaration
class DurationField(UUIDMixIn, DurationField):

    def __init__(self, read_only=False, write_only=False, required=None, default=fields.empty, initial=fields.empty,
                 source=None, label=None, help_text=None, style=None, error_messages=None, validators=None,
                 allow_null=False, uuid: UUID=None, **kw):
        kwargs = {k: v for k, v in locals().items() if not k.startswith(('__', 'self', 'kw'))}
        kwargs.update(kw)
        super().__init__(**kwargs)


# noinspection PyRedeclaration
class ChoiceField(UUIDMixIn, ChoiceField):

    def __init__(self, choices, read_only=False, write_only=False, required=None, default=fields.empty,
                 initial=fields.empty, source=None, label=None, help_text=None, style=None, error_messages=None,
                 validators=None, allow_null=False, uuid: UUID=None, **kw):
        kwargs = {k: v for k, v in locals().items() if not k.startswith(('__', 'self', 'kw'))}
        kwargs.update(kw)
        super().__init__(**kwargs)


# noinspection PyRedeclaration
class MultipleChoiceField(UUIDMixIn, MultipleChoiceField):

    def __init__(self, choices, read_only=False, write_only=False, required=None, default=fields.empty,
                 initial=fields.empty, source=None, label=None, help_text=None, style=None, error_messages=None,
                 validators=None, allow_null=False, uuid: UUID=None, **kw):
        kwargs = {k: v for k, v in locals().items() if not k.startswith(('__', 'self', 'kw'))}
        kwargs.update(kw)
        super().__init__(**kwargs)


# noinspection PyRedeclaration
class FilePathField(UUIDMixIn, FilePathField):

    def __init__(self, path, match=None, recursive=False, allow_files=True, allow_folders=False, required=None,
                 read_only=False, write_only=False, default=fields.empty, initial=fields.empty, source=None, label=None,
                 help_text=None, style=None, error_messages=None, validators=None, allow_null=False, uuid: UUID=None,
                 **kw):
        kwargs = {k: v for k, v in locals().items() if not k.startswith(('__', 'self', 'kw'))}
        kwargs.update(kw)
        super().__init__(**kwargs)


# noinspection PyRedeclaration
class FileField(UUIDMixIn, FileField):

    def __init__(self, read_only=False, write_only=False, required=None, default=fields.empty, initial=fields.empty,
                 source=None, label=None, help_text=None, style=None, error_messages=None, validators=None,
                 allow_null=False, uuid: UUID=None, **kw):
        kwargs = {k: v for k, v in locals().items() if not k.startswith(('__', 'self', 'kw'))}
        kwargs.update(kw)
        super().__init__(**kwargs)


# noinspection PyRedeclaration
class ImageField(UUIDMixIn, ImageField):

    def __init__(self, read_only=False, write_only=False, required=None, default=fields.empty, initial=fields.empty,
                 source=None, label=None, help_text=None, style=None, error_messages=None, validators=None,
                 allow_null=False, uuid: UUID=None, **kw):
        kwargs = {k: v for k, v in locals().items() if not k.startswith(('__', 'self', 'kw'))}
        kwargs.update(kw)
        super().__init__(**kwargs)


# noinspection PyRedeclaration
class ListField(UUIDMixIn, ListField):

    def __init__(self, read_only=False, write_only=False, required=None, default=fields.empty, initial=fields.empty,
                 source=None, label=None, help_text=None, style=None, error_messages=None, validators=None,
                 allow_null=False, uuid: UUID=None, **kw):
        kwargs = {k: v for k, v in locals().items() if not k.startswith(('__', 'self', 'kw'))}
        kwargs.update(kw)
        super().__init__(**kwargs)


# noinspection PyRedeclaration
class DictField(UUIDMixIn, DictField):

    def __init__(self, read_only=False, write_only=False, required=None, default=fields.empty, initial=fields.empty,
                 source=None, label=None, help_text=None, style=None, error_messages=None, validators=None,
                 allow_null=False, uuid: UUID=None, **kw):
        kwargs = {k: v for k, v in locals().items() if not k.startswith(('__', 'self', 'kw'))}
        kwargs.update(kw)
        super().__init__(**kwargs)


# noinspection PyRedeclaration
class HStoreField(UUIDMixIn, HStoreField):

    def __init__(self, read_only=False, write_only=False, required=None, default=fields.empty, initial=fields.empty,
                 source=None, label=None, help_text=None, style=None, error_messages=None, validators=None,
                 allow_null=False, uuid: UUID=None, **kw):
        kwargs = {k: v for k, v in locals().items() if not k.startswith(('__', 'self', 'kw'))}
        kwargs.update(kw)
        super().__init__(**kwargs)


# noinspection PyRedeclaration
class JSONField(UUIDMixIn, JSONField):

    def __init__(self, read_only=False, write_only=False, required=None, default=fields.empty, initial=fields.empty,
                 source=None, label=None, help_text=None, style=None, error_messages=None, validators=None,
                 allow_null=False, uuid: UUID=None, **kw):
        kwargs = {k: v for k, v in locals().items() if not k.startswith(('__', 'self', 'kw'))}
        kwargs.update(kw)
        super().__init__(**kwargs)


# noinspection PyRedeclaration,PyAbstractClass
class ReadOnlyField(UUIDMixIn, ReadOnlyField):

    def __init__(self, read_only=False, write_only=False, required=None, default=fields.empty, initial=fields.empty,
                 source=None, label=None, help_text=None, style=None, error_messages=None, validators=None,
                 allow_null=False, uuid: UUID=None, **kw):
        kwargs = {k: v for k, v in locals().items() if not k.startswith(('__', 'self', 'kw'))}
        kwargs.update(kw)
        super().__init__(**kwargs)


# noinspection PyRedeclaration,PyAbstractClass
class HiddenField(UUIDMixIn, HiddenField):

    def __init__(self, read_only=False, write_only=False, required=None, default=fields.empty, initial=fields.empty,
                 source=None, label=None, help_text=None, style=None, error_messages=None, validators=None,
                 allow_null=False, uuid: UUID=None, **kw):
        kwargs = {k: v for k, v in locals().items() if not k.startswith(('__', 'self', 'kw'))}
        kwargs.update(kw)
        super().__init__(**kwargs)


# noinspection PyRedeclaration,PyAbstractClass
class SerializerMethodField(UUIDMixIn, SerializerMethodField):

    def __init__(self, method_name=None, read_only=False, write_only=False, required=None, default=fields.empty,
                 initial=fields.empty, source=None, label=None, help_text=None, style=None, error_messages=None,
                 validators=None, allow_null=False, uuid: UUID=None, **kw):
        kwargs = {k: v for k, v in locals().items() if not k.startswith(('__', 'self', 'kw'))}
        kwargs.update(kw)
        super().__init__(**kwargs)


# noinspection PyRedeclaration
class ModelField(UUIDMixIn, ModelField):

    def __init__(self, model_field, read_only=False, write_only=False, required=None, default=fields.empty,
                 initial=fields.empty, source=None, label=None, help_text=None, style=None, error_messages=None,
                 validators=None, allow_null=False, uuid: UUID=None, **kw):
        kwargs = {k: v for k, v in locals().items() if not k.startswith(('__', 'self', 'kw'))}
        kwargs.update(kw)
        super().__init__(**kwargs)
