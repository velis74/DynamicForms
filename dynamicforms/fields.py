from uuid import UUID

from rest_framework import fields
from rest_framework.fields import (
    BooleanField, NullBooleanField, CharField, EmailField, RegexField, SlugField, URLField, UUIDField,
    IPAddressField, IntegerField, FloatField, DecimalField, DateTimeField, DateField, TimeField, DurationField,
    ChoiceField, MultipleChoiceField, FilePathField, FileField, ImageField, ListField, DictField, HStoreField,
    JSONField, ReadOnlyField, HiddenField, SerializerMethodField, ModelField
)
from rest_framework.relations import (
    StringRelatedField, PrimaryKeyRelatedField, HyperlinkedRelatedField, HyperlinkedIdentityField,
    SlugRelatedField
)
from .mixins import ActionMixin, RenderToTableMixin, UUIDMixIn


# noinspection PyRedeclaration
class BooleanField(UUIDMixIn, ActionMixin, RenderToTableMixin, BooleanField):

    def __init__(self, read_only=False, write_only=False, required=None, default=fields.empty, initial=fields.empty,
                 source=None, label=None, help_text=None, style=None, error_messages=None, validators=None,
                 uuid: UUID=None, **kw):
        kwargs = {k: v for k, v in locals().items() if not k.startswith(('__', 'self', 'kw'))}
        kwargs.update(kw)
        super().__init__(**kwargs)


# noinspection PyRedeclaration
class NullBooleanField(UUIDMixIn, ActionMixin, RenderToTableMixin, NullBooleanField):

    def __init__(self, read_only=False, write_only=False, required=None, default=fields.empty, initial=fields.empty,
                 source=None, label=None, help_text=None, style=None, error_messages=None, validators=None,
                 allow_null=False, uuid: UUID=None, **kw):
        kwargs = {k: v for k, v in locals().items() if not k.startswith(('__', 'self', 'kw'))}
        kwargs.update(kw)
        super().__init__(**kwargs)


# noinspection PyRedeclaration
class CharField(UUIDMixIn, ActionMixin, RenderToTableMixin, CharField):

    def __init__(self, read_only=False, write_only=False, required=None, default=fields.empty, initial=fields.empty,
                 source=None, label=None, help_text=None, style=None, error_messages=None, validators=None,
                 allow_null=False, uuid: UUID=None, **kw):
        kwargs = {k: v for k, v in locals().items() if not k.startswith(('__', 'self', 'kw'))}
        kwargs.update(kw)
        super().__init__(**kwargs)


# noinspection PyRedeclaration
class EmailField(UUIDMixIn, ActionMixin, RenderToTableMixin, EmailField):

    def __init__(self, read_only=False, write_only=False, required=None, default=fields.empty, initial=fields.empty,
                 source=None, label=None, help_text=None, style=None, error_messages=None, validators=None,
                 allow_null=False, uuid: UUID=None, **kw):
        kwargs = {k: v for k, v in locals().items() if not k.startswith(('__', 'self', 'kw'))}
        kwargs.update(kw)
        super().__init__(**kwargs)


# noinspection PyRedeclaration
class RegexField(UUIDMixIn, ActionMixin, RenderToTableMixin, RegexField):

    def __init__(self, regex, read_only=False, write_only=False, required=None, default=fields.empty,
                 initial=fields.empty, source=None, label=None, help_text=None, style=None, error_messages=None,
                 validators=None, allow_null=False, uuid: UUID=None, **kw):
        kwargs = {k: v for k, v in locals().items() if not k.startswith(('__', 'self', 'kw'))}
        kwargs.update(kw)
        super().__init__(**kwargs)


# noinspection PyRedeclaration
class SlugField(UUIDMixIn, ActionMixin, RenderToTableMixin, SlugField):

    def __init__(self, allow_unicode=False, read_only=False, write_only=False, required=None, default=fields.empty,
                 initial=fields.empty, source=None, label=None, help_text=None, style=None, error_messages=None,
                 validators=None, allow_null=False, uuid: UUID=None, **kw):
        kwargs = {k: v for k, v in locals().items() if not k.startswith(('__', 'self', 'kw'))}
        kwargs.update(kw)
        super().__init__(**kwargs)


# noinspection PyRedeclaration
class URLField(UUIDMixIn, ActionMixin, RenderToTableMixin, URLField):

    def __init__(self, read_only=False, write_only=False, required=None, default=fields.empty, initial=fields.empty,
                 source=None, label=None, help_text=None, style=None, error_messages=None, validators=None,
                 allow_null=False, uuid: UUID=None, **kw):
        kwargs = {k: v for k, v in locals().items() if not k.startswith(('__', 'self', 'kw'))}
        kwargs.update(kw)
        super().__init__(**kwargs)


# noinspection PyRedeclaration
class UUIDField(UUIDMixIn, ActionMixin, RenderToTableMixin, UUIDField):

    def __init__(self, read_only=False, write_only=False, required=None, default=fields.empty, initial=fields.empty,
                 source=None, label=None, help_text=None, style=None, error_messages=None, validators=None,
                 allow_null=False, uuid: UUID=None, **kw):
        kwargs = {k: v for k, v in locals().items() if not k.startswith(('__', 'self', 'kw'))}
        kwargs.update(kw)
        super().__init__(**kwargs)


# noinspection PyRedeclaration
class IPAddressField(UUIDMixIn, ActionMixin, RenderToTableMixin, IPAddressField):

    def __init__(self, protocol='both', read_only=False, write_only=False, required=None, default=fields.empty,
                 initial=fields.empty, source=None, label=None, help_text=None, style=None, error_messages=None,
                 validators=None, allow_null=False, uuid: UUID=None, **kw):
        kwargs = {k: v for k, v in locals().items() if not k.startswith(('__', 'self', 'kw'))}
        kwargs.update(kw)
        super().__init__(**kwargs)


# noinspection PyRedeclaration
class IntegerField(UUIDMixIn, ActionMixin, RenderToTableMixin, IntegerField):

    def __init__(self, read_only=False, write_only=False, required=None, default=fields.empty, initial=fields.empty,
                 source=None, label=None, help_text=None, style=None, error_messages=None, validators=None,
                 allow_null=False, uuid: UUID=None, **kw):
        kwargs = {k: v for k, v in locals().items() if not k.startswith(('__', 'self', 'kw'))}
        kwargs.update(kw)
        super().__init__(**kwargs)


# noinspection PyRedeclaration
class FloatField(UUIDMixIn, ActionMixin, RenderToTableMixin, FloatField):

    def __init__(self, read_only=False, write_only=False, required=None, default=fields.empty, initial=fields.empty,
                 source=None, label=None, help_text=None, style=None, error_messages=None, validators=None,
                 allow_null=False, uuid: UUID=None, **kw):
        kwargs = {k: v for k, v in locals().items() if not k.startswith(('__', 'self', 'kw'))}
        kwargs.update(kw)
        super().__init__(**kwargs)


# noinspection PyRedeclaration
class DecimalField(UUIDMixIn, ActionMixin, RenderToTableMixin, DecimalField):

    def __init__(self, max_digits, decimal_places, coerce_to_string=None, max_value=None, min_value=None,
                 localize=False, rounding=None, read_only=False, write_only=False, required=None, default=fields.empty,
                 initial=fields.empty, source=None, label=None, help_text=None, style=None, error_messages=None,
                 validators=None, allow_null=False, uuid: UUID=None, **kw):
        kwargs = {k: v for k, v in locals().items() if not k.startswith(('__', 'self', 'kw'))}
        kwargs.update(kw)
        super().__init__(**kwargs)


# noinspection PyRedeclaration,PyShadowingBuiltins
class DateTimeField(UUIDMixIn, ActionMixin, RenderToTableMixin, DateTimeField):

    def __init__(self, format=fields.empty, input_formats=None, default_timezone=None, read_only=False,
                 write_only=False, required=None, default=fields.empty, initial=fields.empty, source=None, label=None,
                 help_text=None, style=None, error_messages=None, validators=None, allow_null=False, uuid: UUID=None,
                 **kw):
        kwargs = {k: v for k, v in locals().items() if not k.startswith(('__', 'self', 'kw'))}
        kwargs.update(kw)
        super().__init__(**kwargs)


# noinspection PyRedeclaration,PyShadowingBuiltins
class DateField(UUIDMixIn, ActionMixin, RenderToTableMixin, DateField):

    def __init__(self, format=fields.empty, input_formats=None, read_only=False, write_only=False, required=None,
                 default=fields.empty, initial=fields.empty, source=None, label=None, help_text=None, style=None,
                 error_messages=None, validators=None, allow_null=False, uuid: UUID=None, **kw):
        kwargs = {k: v for k, v in locals().items() if not k.startswith(('__', 'self', 'kw'))}
        kwargs.update(kw)
        super().__init__(**kwargs)


# noinspection PyRedeclaration,PyShadowingBuiltins
class TimeField(UUIDMixIn, ActionMixin, RenderToTableMixin, TimeField):

    def __init__(self, format=fields.empty, input_formats=None, read_only=False, write_only=False, required=None,
                 default=fields.empty, initial=fields.empty, source=None, label=None, help_text=None, style=None,
                 error_messages=None, validators=None, allow_null=False, uuid: UUID=None, **kw):
        kwargs = {k: v for k, v in locals().items() if not k.startswith(('__', 'self', 'kw'))}
        kwargs.update(kw)
        super().__init__(**kwargs)


# noinspection PyRedeclaration
class DurationField(UUIDMixIn, ActionMixin, RenderToTableMixin, DurationField):

    def __init__(self, read_only=False, write_only=False, required=None, default=fields.empty, initial=fields.empty,
                 source=None, label=None, help_text=None, style=None, error_messages=None, validators=None,
                 allow_null=False, uuid: UUID=None, **kw):
        kwargs = {k: v for k, v in locals().items() if not k.startswith(('__', 'self', 'kw'))}
        kwargs.update(kw)
        super().__init__(**kwargs)


# noinspection PyRedeclaration
class ChoiceField(UUIDMixIn, ActionMixin, RenderToTableMixin, ChoiceField):

    def __init__(self, choices, read_only=False, write_only=False, required=None, default=fields.empty,
                 initial=fields.empty, source=None, label=None, help_text=None, style=None, error_messages=None,
                 validators=None, allow_null=False, uuid: UUID=None, **kw):
        kwargs = {k: v for k, v in locals().items() if not k.startswith(('__', 'self', 'kw'))}
        kwargs.update(kw)
        super().__init__(**kwargs)


# noinspection PyRedeclaration
class MultipleChoiceField(UUIDMixIn, ActionMixin, RenderToTableMixin, MultipleChoiceField):

    def __init__(self, choices, read_only=False, write_only=False, required=None, default=fields.empty,
                 initial=fields.empty, source=None, label=None, help_text=None, style=None, error_messages=None,
                 validators=None, allow_null=False, uuid: UUID=None, **kw):
        kwargs = {k: v for k, v in locals().items() if not k.startswith(('__', 'self', 'kw'))}
        kwargs.update(kw)
        super().__init__(**kwargs)


# noinspection PyRedeclaration
class FilePathField(UUIDMixIn, ActionMixin, RenderToTableMixin, FilePathField):

    def __init__(self, path, match=None, recursive=False, allow_files=True, allow_folders=False, required=None,
                 read_only=False, write_only=False, default=fields.empty, initial=fields.empty, source=None, label=None,
                 help_text=None, style=None, error_messages=None, validators=None, allow_null=False, uuid: UUID=None,
                 **kw):
        kwargs = {k: v for k, v in locals().items() if not k.startswith(('__', 'self', 'kw'))}
        kwargs.update(kw)
        super().__init__(**kwargs)


# noinspection PyRedeclaration
class FileField(UUIDMixIn, ActionMixin, RenderToTableMixin, FileField):

    def __init__(self, read_only=False, write_only=False, required=None, default=fields.empty, initial=fields.empty,
                 source=None, label=None, help_text=None, style=None, error_messages=None, validators=None,
                 allow_null=False, uuid: UUID=None, **kw):
        kwargs = {k: v for k, v in locals().items() if not k.startswith(('__', 'self', 'kw'))}
        kwargs.update(kw)
        super().__init__(**kwargs)


# noinspection PyRedeclaration
class ImageField(UUIDMixIn, ActionMixin, RenderToTableMixin, ImageField):

    def __init__(self, read_only=False, write_only=False, required=None, default=fields.empty, initial=fields.empty,
                 source=None, label=None, help_text=None, style=None, error_messages=None, validators=None,
                 allow_null=False, uuid: UUID=None, **kw):
        kwargs = {k: v for k, v in locals().items() if not k.startswith(('__', 'self', 'kw'))}
        kwargs.update(kw)
        super().__init__(**kwargs)


# noinspection PyRedeclaration
class ListField(UUIDMixIn, ActionMixin, RenderToTableMixin, ListField):

    def __init__(self, read_only=False, write_only=False, required=None, default=fields.empty, initial=fields.empty,
                 source=None, label=None, help_text=None, style=None, error_messages=None, validators=None,
                 allow_null=False, uuid: UUID=None, **kw):
        kwargs = {k: v for k, v in locals().items() if not k.startswith(('__', 'self', 'kw'))}
        kwargs.update(kw)
        super().__init__(**kwargs)


# noinspection PyRedeclaration
class DictField(UUIDMixIn, ActionMixin, RenderToTableMixin, DictField):

    def __init__(self, read_only=False, write_only=False, required=None, default=fields.empty, initial=fields.empty,
                 source=None, label=None, help_text=None, style=None, error_messages=None, validators=None,
                 allow_null=False, uuid: UUID=None, **kw):
        kwargs = {k: v for k, v in locals().items() if not k.startswith(('__', 'self', 'kw'))}
        kwargs.update(kw)
        super().__init__(**kwargs)


# noinspection PyRedeclaration
class HStoreField(UUIDMixIn, ActionMixin, RenderToTableMixin, HStoreField):

    def __init__(self, read_only=False, write_only=False, required=None, default=fields.empty, initial=fields.empty,
                 source=None, label=None, help_text=None, style=None, error_messages=None, validators=None,
                 allow_null=False, uuid: UUID=None, **kw):
        kwargs = {k: v for k, v in locals().items() if not k.startswith(('__', 'self', 'kw'))}
        kwargs.update(kw)
        super().__init__(**kwargs)


# noinspection PyRedeclaration
class JSONField(UUIDMixIn, ActionMixin, RenderToTableMixin, JSONField):

    def __init__(self, read_only=False, write_only=False, required=None, default=fields.empty, initial=fields.empty,
                 source=None, label=None, help_text=None, style=None, error_messages=None, validators=None,
                 allow_null=False, uuid: UUID=None, **kw):
        kwargs = {k: v for k, v in locals().items() if not k.startswith(('__', 'self', 'kw'))}
        kwargs.update(kw)
        super().__init__(**kwargs)


# noinspection PyRedeclaration,PyAbstractClass
class ReadOnlyField(UUIDMixIn, ActionMixin, RenderToTableMixin, ReadOnlyField):

    def __init__(self, read_only=False, write_only=False, required=None, default=fields.empty, initial=fields.empty,
                 source=None, label=None, help_text=None, style=None, error_messages=None, validators=None,
                 allow_null=False, uuid: UUID=None, **kw):
        kwargs = {k: v for k, v in locals().items() if not k.startswith(('__', 'self', 'kw'))}
        kwargs.update(kw)
        super().__init__(**kwargs)


# noinspection PyRedeclaration,PyAbstractClass
class HiddenField(UUIDMixIn, ActionMixin, RenderToTableMixin, HiddenField):

    def __init__(self, read_only=False, write_only=False, required=None, default=fields.empty, initial=fields.empty,
                 source=None, label=None, help_text=None, style=None, error_messages=None, validators=None,
                 allow_null=False, uuid: UUID=None, **kw):
        kwargs = {k: v for k, v in locals().items() if not k.startswith(('__', 'self', 'kw'))}
        kwargs.update(kw)
        super().__init__(**kwargs)


# noinspection PyRedeclaration,PyAbstractClass
class SerializerMethodField(UUIDMixIn, ActionMixin, RenderToTableMixin, SerializerMethodField):

    def __init__(self, method_name=None, read_only=False, write_only=False, required=None, default=fields.empty,
                 initial=fields.empty, source=None, label=None, help_text=None, style=None, error_messages=None,
                 validators=None, allow_null=False, uuid: UUID=None, **kw):
        kwargs = {k: v for k, v in locals().items() if not k.startswith(('__', 'self', 'kw'))}
        kwargs.update(kw)
        super().__init__(**kwargs)


# noinspection PyRedeclaration
class ModelField(UUIDMixIn, ActionMixin, RenderToTableMixin, ModelField):

    def __init__(self, model_field, read_only=False, write_only=False, required=None, default=fields.empty,
                 initial=fields.empty, source=None, label=None, help_text=None, style=None, error_messages=None,
                 validators=None, allow_null=False, uuid: UUID=None, **kw):
        kwargs = {k: v for k, v in locals().items() if not k.startswith(('__', 'self', 'kw'))}
        kwargs.update(kw)
        super().__init__(**kwargs)


# noinspection PyRedeclaration
class StringRelatedField(UUIDMixIn, ActionMixin, RenderToTableMixin, StringRelatedField):

    def __init__(self, read_only=False, write_only=False, required=None, default=fields.empty, initial=fields.empty,
                 source=None, label=None, help_text=None, style=None, error_messages=None, validators=None,
                 allow_null=False, uuid: UUID=None, **kw):
        kwargs = {k: v for k, v in locals().items() if not k.startswith(('__', 'self', 'kw'))}
        kwargs.update(kw)
        super().__init__(**kwargs)


# noinspection PyRedeclaration
class PrimaryKeyRelatedField(UUIDMixIn, ActionMixin, RenderToTableMixin, PrimaryKeyRelatedField):

    def __init__(self, read_only=False, write_only=False, required=None, default=fields.empty, initial=fields.empty,
                 source=None, label=None, help_text=None, style=None, error_messages=None, validators=None,
                 allow_null=False, uuid: UUID=None, **kw):
        kwargs = {k: v for k, v in locals().items() if not k.startswith(('__', 'self', 'kw'))}
        kwargs.update(kw)
        super().__init__(**kwargs)


# noinspection PyRedeclaration
class HyperlinkedRelatedField(UUIDMixIn, ActionMixin, RenderToTableMixin, HyperlinkedRelatedField):

    def __init__(self, view_name=None, read_only=False, write_only=False, required=None, default=fields.empty,
                 initial=fields.empty, source=None, label=None, help_text=None, style=None, error_messages=None,
                 validators=None, allow_null=False, uuid: UUID=None, **kw):
        kwargs = {k: v for k, v in locals().items() if not k.startswith(('__', 'self', 'kw'))}
        kwargs.update(kw)
        super().__init__(**kwargs)


# noinspection PyRedeclaration
class HyperlinkedIdentityField(UUIDMixIn, ActionMixin, RenderToTableMixin, HyperlinkedIdentityField):

    def __init__(self, view_name=None, read_only=False, write_only=False, required=None, default=fields.empty,
                 initial=fields.empty, source=None, label=None, help_text=None, style=None, error_messages=None,
                 validators=None, allow_null=False, uuid: UUID=None, **kw):
        kwargs = {k: v for k, v in locals().items() if not k.startswith(('__', 'self', 'kw'))}
        kwargs.update(kw)
        super().__init__(**kwargs)


# noinspection PyRedeclaration
class SlugRelatedField(UUIDMixIn, ActionMixin, RenderToTableMixin, SlugRelatedField):

    def __init__(self, slug_field=None, read_only=False, write_only=False, required=None, default=fields.empty,
                 initial=fields.empty, source=None, label=None, help_text=None, style=None, error_messages=None,
                 validators=None, allow_null=False, uuid: UUID=None, **kw):
        kwargs = {k: v for k, v in locals().items() if not k.startswith(('__', 'self', 'kw'))}
        kwargs.update(kw)
        super().__init__(**kwargs)
