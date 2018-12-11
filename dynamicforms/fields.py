from uuid import UUID

from rest_framework import fields, relations

from .mixins import ActionMixin, RenderToTableMixin, UUIDMixIn


# noinspection PyRedeclaration
class BooleanField(UUIDMixIn, ActionMixin, RenderToTableMixin, fields.BooleanField):

    def __init__(self, read_only=False, write_only=False, required=None, default=fields.empty, initial=fields.empty,
                 source=None, label=None, help_text=None, style=None, error_messages=None, validators=None,
                 uuid: UUID=None, **kw):
        kwargs = {k: v for k, v in locals().items() if not k.startswith(('__', 'self', 'kw'))}
        kwargs.update(kw)
        super().__init__(**kwargs)


# noinspection PyRedeclaration
"""
class NullBooleanField(UUIDMixIn, ActionMixin, RenderToTableMixin, fields.NullBooleanField):

    def __init__(self, read_only=False, write_only=False, required=None, default=fields.empty, initial=fields.empty,
                 source=None, label=None, help_text=None, style=None, error_messages=None, validators=None,
                 allow_null=False, uuid: UUID=None, **kw):
        kwargs = {k: v for k, v in locals().items() if not k.startswith(('__', 'self', 'kw'))}
        kwargs.update(kw)
        super().__init__(**kwargs)
"""

# Without allow_null=False kwarg, which throws error AssertionError: `allow_null` is not a valid option.
# noinspection PyRedeclaration
class NullBooleanField(UUIDMixIn, ActionMixin, RenderToTableMixin, fields.NullBooleanField):

    def __init__(self, read_only=False, write_only=False, required=None, default=fields.empty, initial=fields.empty,
                 source=None, label=None, help_text=None, style=None, error_messages=None, validators=None,
                 uuid: UUID=None, **kw):
        kwargs = {k: v for k, v in locals().items() if not k.startswith(('__', 'self', 'kw'))}
        kwargs.update(kw)
        super().__init__(**kwargs)


# noinspection PyRedeclaration
class CharField(UUIDMixIn, ActionMixin, RenderToTableMixin, fields.CharField):

    def __init__(self, read_only=False, write_only=False, required=None, default=fields.empty, initial=fields.empty,
                 source=None, label=None, help_text=None, style=None, error_messages=None, validators=None,
                 allow_null=False, uuid: UUID=None, **kw):
        kwargs = {k: v for k, v in locals().items() if not k.startswith(('__', 'self', 'kw'))}
        kwargs.update(kw)
        super().__init__(**kwargs)


# noinspection PyRedeclaration
class EmailField(UUIDMixIn, ActionMixin, RenderToTableMixin, fields.EmailField):

    def __init__(self, read_only=False, write_only=False, required=None, default=fields.empty, initial=fields.empty,
                 source=None, label=None, help_text=None, style=None, error_messages=None, validators=None,
                 allow_null=False, uuid: UUID=None, **kw):
        kwargs = {k: v for k, v in locals().items() if not k.startswith(('__', 'self', 'kw'))}
        kwargs.update(kw)
        super().__init__(**kwargs)


# noinspection PyRedeclaration
class RegexField(UUIDMixIn, ActionMixin, RenderToTableMixin, fields.RegexField):

    def __init__(self, regex, read_only=False, write_only=False, required=None, default=fields.empty,
                 initial=fields.empty, source=None, label=None, help_text=None, style=None, error_messages=None,
                 validators=None, allow_null=False, uuid: UUID=None, **kw):
        kwargs = {k: v for k, v in locals().items() if not k.startswith(('__', 'self', 'kw'))}
        kwargs.update(kw)
        super().__init__(**kwargs)


# noinspection PyRedeclaration
class SlugField(UUIDMixIn, ActionMixin, RenderToTableMixin, fields.SlugField):

    def __init__(self, allow_unicode=False, read_only=False, write_only=False, required=None, default=fields.empty,
                 initial=fields.empty, source=None, label=None, help_text=None, style=None, error_messages=None,
                 validators=None, allow_null=False, uuid: UUID=None, **kw):
        kwargs = {k: v for k, v in locals().items() if not k.startswith(('__', 'self', 'kw'))}
        kwargs.update(kw)
        super().__init__(**kwargs)


# noinspection PyRedeclaration
class URLField(UUIDMixIn, ActionMixin, RenderToTableMixin, fields.URLField):

    def __init__(self, read_only=False, write_only=False, required=None, default=fields.empty, initial=fields.empty,
                 source=None, label=None, help_text=None, style=None, error_messages=None, validators=None,
                 allow_null=False, uuid: UUID=None, **kw):
        kwargs = {k: v for k, v in locals().items() if not k.startswith(('__', 'self', 'kw'))}
        kwargs.update(kw)
        super().__init__(**kwargs)


# noinspection PyRedeclaration
class UUIDField(UUIDMixIn, ActionMixin, RenderToTableMixin, fields.UUIDField):

    def __init__(self, read_only=False, write_only=False, required=None, default=fields.empty, initial=fields.empty,
                 source=None, label=None, help_text=None, style=None, error_messages=None, validators=None,
                 allow_null=False, uuid: UUID=None, **kw):
        kwargs = {k: v for k, v in locals().items() if not k.startswith(('__', 'self', 'kw'))}
        kwargs.update(kw)
        super().__init__(**kwargs)


# noinspection PyRedeclaration
class IPAddressField(UUIDMixIn, ActionMixin, RenderToTableMixin, fields.IPAddressField):

    def __init__(self, protocol='both', read_only=False, write_only=False, required=None, default=fields.empty,
                 initial=fields.empty, source=None, label=None, help_text=None, style=None, error_messages=None,
                 validators=None, allow_null=False, uuid: UUID=None, **kw):
        kwargs = {k: v for k, v in locals().items() if not k.startswith(('__', 'self', 'kw'))}
        kwargs.update(kw)
        super().__init__(**kwargs)


# noinspection PyRedeclaration
class IntegerField(UUIDMixIn, ActionMixin, RenderToTableMixin, fields.IntegerField):

    def __init__(self, read_only=False, write_only=False, required=None, default=fields.empty, initial=fields.empty,
                 source=None, label=None, help_text=None, style=None, error_messages=None, validators=None,
                 allow_null=False, uuid: UUID=None, **kw):
        kwargs = {k: v for k, v in locals().items() if not k.startswith(('__', 'self', 'kw'))}
        kwargs.update(kw)
        super().__init__(**kwargs)


# noinspection PyRedeclaration
class FloatField(UUIDMixIn, ActionMixin, RenderToTableMixin, fields.FloatField):

    def __init__(self, read_only=False, write_only=False, required=None, default=fields.empty, initial=fields.empty,
                 source=None, label=None, help_text=None, style=None, error_messages=None, validators=None,
                 allow_null=False, uuid: UUID=None, **kw):
        kwargs = {k: v for k, v in locals().items() if not k.startswith(('__', 'self', 'kw'))}
        kwargs.update(kw)
        super().__init__(**kwargs)


# noinspection PyRedeclaration
class DecimalField(UUIDMixIn, ActionMixin, RenderToTableMixin, fields.DecimalField):

    def __init__(self, max_digits, decimal_places, coerce_to_string=None, max_value=None, min_value=None,
                 localize=False, rounding=None, read_only=False, write_only=False, required=None, default=fields.empty,
                 initial=fields.empty, source=None, label=None, help_text=None, style=None, error_messages=None,
                 validators=None, allow_null=False, uuid: UUID=None, **kw):
        kwargs = {k: v for k, v in locals().items() if not k.startswith(('__', 'self', 'kw'))}
        kwargs.update(kw)
        super().__init__(**kwargs)


# noinspection PyRedeclaration,PyShadowingBuiltins
class DateTimeField(UUIDMixIn, ActionMixin, RenderToTableMixin, fields.DateTimeField):

    def __init__(self, format=fields.empty, input_formats=None, default_timezone=None, read_only=False,
                 write_only=False, required=None, default=fields.empty, initial=fields.empty, source=None, label=None,
                 help_text=None, style=None, error_messages=None, validators=None, allow_null=False, uuid: UUID=None,
                 **kw):
        kwargs = {k: v for k, v in locals().items() if not k.startswith(('__', 'self', 'kw'))}
        kwargs.update(kw)
        super().__init__(**kwargs)


# noinspection PyRedeclaration,PyShadowingBuiltins
class DateField(UUIDMixIn, ActionMixin, RenderToTableMixin, fields.DateField):

    def __init__(self, format=fields.empty, input_formats=None, read_only=False, write_only=False, required=None,
                 default=fields.empty, initial=fields.empty, source=None, label=None, help_text=None, style=None,
                 error_messages=None, validators=None, allow_null=False, uuid: UUID=None, **kw):
        kwargs = {k: v for k, v in locals().items() if not k.startswith(('__', 'self', 'kw'))}
        kwargs.update(kw)
        super().__init__(**kwargs)


# noinspection PyRedeclaration,PyShadowingBuiltins
class TimeField(UUIDMixIn, ActionMixin, RenderToTableMixin, fields.TimeField):

    def __init__(self, format=fields.empty, input_formats=None, read_only=False, write_only=False, required=None,
                 default=fields.empty, initial=fields.empty, source=None, label=None, help_text=None, style=None,
                 error_messages=None, validators=None, allow_null=False, uuid: UUID=None, **kw):
        kwargs = {k: v for k, v in locals().items() if not k.startswith(('__', 'self', 'kw'))}
        kwargs.update(kw)
        super().__init__(**kwargs)


# noinspection PyRedeclaration
class DurationField(UUIDMixIn, ActionMixin, RenderToTableMixin, fields.DurationField):

    def __init__(self, read_only=False, write_only=False, required=None, default=fields.empty, initial=fields.empty,
                 source=None, label=None, help_text=None, style=None, error_messages=None, validators=None,
                 allow_null=False, uuid: UUID=None, **kw):
        kwargs = {k: v for k, v in locals().items() if not k.startswith(('__', 'self', 'kw'))}
        kwargs.update(kw)
        super().__init__(**kwargs)


# noinspection PyRedeclaration
class ChoiceField(UUIDMixIn, ActionMixin, RenderToTableMixin, fields.ChoiceField):

    def __init__(self, choices, read_only=False, write_only=False, required=None, default=fields.empty,
                 initial=fields.empty, source=None, label=None, help_text=None, style=None, error_messages=None,
                 validators=None, allow_null=False, uuid: UUID=None, **kw):
        kwargs = {k: v for k, v in locals().items() if not k.startswith(('__', 'self', 'kw'))}
        kwargs.update(kw)
        super().__init__(**kwargs)


# noinspection PyRedeclaration
class MultipleChoiceField(UUIDMixIn, ActionMixin, RenderToTableMixin, fields.MultipleChoiceField):

    def __init__(self, choices, read_only=False, write_only=False, required=None, default=fields.empty,
                 initial=fields.empty, source=None, label=None, help_text=None, style=None, error_messages=None,
                 validators=None, allow_null=False, uuid: UUID=None, **kw):
        kwargs = {k: v for k, v in locals().items() if not k.startswith(('__', 'self', 'kw'))}
        kwargs.update(kw)
        super().__init__(**kwargs)


# noinspection PyRedeclaration
class FilePathField(UUIDMixIn, ActionMixin, RenderToTableMixin, fields.FilePathField):

    def __init__(self, path, match=None, recursive=False, allow_files=True, allow_folders=False, required=None,
                 read_only=False, write_only=False, default=fields.empty, initial=fields.empty, source=None, label=None,
                 help_text=None, style=None, error_messages=None, validators=None, allow_null=False, uuid: UUID=None,
                 **kw):
        kwargs = {k: v for k, v in locals().items() if not k.startswith(('__', 'self', 'kw'))}
        kwargs.update(kw)
        super().__init__(**kwargs)


# noinspection PyRedeclaration
class FileField(UUIDMixIn, ActionMixin, RenderToTableMixin, fields.FileField):

    def __init__(self, read_only=False, write_only=False, required=None, default=fields.empty, initial=fields.empty,
                 source=None, label=None, help_text=None, style=None, error_messages=None, validators=None,
                 allow_null=False, uuid: UUID=None, **kw):
        kwargs = {k: v for k, v in locals().items() if not k.startswith(('__', 'self', 'kw'))}
        kwargs.update(kw)
        super().__init__(**kwargs)


# noinspection PyRedeclaration
class ImageField(UUIDMixIn, ActionMixin, RenderToTableMixin, fields.ImageField):

    def __init__(self, read_only=False, write_only=False, required=None, default=fields.empty, initial=fields.empty,
                 source=None, label=None, help_text=None, style=None, error_messages=None, validators=None,
                 allow_null=False, uuid: UUID=None, **kw):
        kwargs = {k: v for k, v in locals().items() if not k.startswith(('__', 'self', 'kw'))}
        kwargs.update(kw)
        super().__init__(**kwargs)


# noinspection PyRedeclaration
class ListField(UUIDMixIn, ActionMixin, RenderToTableMixin, fields.ListField):

    def __init__(self, read_only=False, write_only=False, required=None, default=fields.empty, initial=fields.empty,
                 source=None, label=None, help_text=None, style=None, error_messages=None, validators=None,
                 allow_null=False, uuid: UUID=None, **kw):
        kwargs = {k: v for k, v in locals().items() if not k.startswith(('__', 'self', 'kw'))}
        kwargs.update(kw)
        super().__init__(**kwargs)


# noinspection PyRedeclaration
class DictField(UUIDMixIn, ActionMixin, RenderToTableMixin, fields.DictField):

    def __init__(self, read_only=False, write_only=False, required=None, default=fields.empty, initial=fields.empty,
                 source=None, label=None, help_text=None, style=None, error_messages=None, validators=None,
                 allow_null=False, uuid: UUID=None, **kw):
        kwargs = {k: v for k, v in locals().items() if not k.startswith(('__', 'self', 'kw'))}
        kwargs.update(kw)
        super().__init__(**kwargs)


# noinspection PyRedeclaration
class JSONField(UUIDMixIn, ActionMixin, RenderToTableMixin, fields.JSONField):

    def __init__(self, read_only=False, write_only=False, required=None, default=fields.empty, initial=fields.empty,
                 source=None, label=None, help_text=None, style=None, error_messages=None, validators=None,
                 allow_null=False, uuid: UUID=None, **kw):
        kwargs = {k: v for k, v in locals().items() if not k.startswith(('__', 'self', 'kw'))}
        kwargs.update(kw)
        super().__init__(**kwargs)


# noinspection PyRedeclaration,PyAbstractClass
class ReadOnlyField(UUIDMixIn, ActionMixin, RenderToTableMixin, fields.ReadOnlyField):

    def __init__(self, read_only=False, write_only=False, required=None, default=fields.empty, initial=fields.empty,
                 source=None, label=None, help_text=None, style=None, error_messages=None, validators=None,
                 allow_null=False, uuid: UUID=None, **kw):
        kwargs = {k: v for k, v in locals().items() if not k.startswith(('__', 'self', 'kw'))}
        kwargs.update(kw)
        super().__init__(**kwargs)


# noinspection PyRedeclaration,PyAbstractClass
class HiddenField(UUIDMixIn, ActionMixin, RenderToTableMixin, fields.HiddenField):

    def __init__(self, visible_in_table=False, read_only=False, write_only=False, required=None, default=fields.empty,
                 initial=fields.empty, source=None, label=None, help_text=None, style=None, error_messages=None,
                 validators=None, allow_null=False, uuid: UUID=None, **kw):
        kwargs = {k: v for k, v in locals().items() if not k.startswith(('__', 'self', 'kw'))}
        kwargs.update(kw)
        super().__init__(**kwargs)


# noinspection PyRedeclaration,PyAbstractClass
class SerializerMethodField(UUIDMixIn, ActionMixin, RenderToTableMixin, fields.SerializerMethodField):

    def __init__(self, method_name=None, read_only=False, write_only=False, required=None, default=fields.empty,
                 initial=fields.empty, source=None, label=None, help_text=None, style=None, error_messages=None,
                 validators=None, allow_null=False, uuid: UUID=None, **kw):
        kwargs = {k: v for k, v in locals().items() if not k.startswith(('__', 'self', 'kw'))}
        kwargs.update(kw)
        super().__init__(**kwargs)


# noinspection PyRedeclaration
class ModelField(UUIDMixIn, ActionMixin, RenderToTableMixin, fields.ModelField):

    def __init__(self, model_field, read_only=False, write_only=False, required=None, default=fields.empty,
                 initial=fields.empty, source=None, label=None, help_text=None, style=None, error_messages=None,
                 validators=None, allow_null=False, uuid: UUID=None, **kw):
        kwargs = {k: v for k, v in locals().items() if not k.startswith(('__', 'self', 'kw'))}
        kwargs.update(kw)
        super().__init__(**kwargs)


# noinspection PyRedeclaration
class StringRelatedField(UUIDMixIn, ActionMixin, RenderToTableMixin, relations.StringRelatedField):

    def __init__(self, read_only=False, write_only=False, required=None, default=fields.empty, initial=fields.empty,
                 source=None, label=None, help_text=None, style=None, error_messages=None, validators=None,
                 allow_null=False, uuid: UUID=None, **kw):
        kwargs = {k: v for k, v in locals().items() if not k.startswith(('__', 'self', 'kw'))}
        kwargs.update(kw)
        super().__init__(**kwargs)


# noinspection PyRedeclaration
class PrimaryKeyRelatedField(UUIDMixIn, ActionMixin, RenderToTableMixin, relations.PrimaryKeyRelatedField):

    def __init__(self, read_only=False, write_only=False, required=None, default=fields.empty, initial=fields.empty,
                 source=None, label=None, help_text=None, style=None, error_messages=None, validators=None,
                 allow_null=False, uuid: UUID=None, **kw):
        kwargs = {k: v for k, v in locals().items() if not k.startswith(('__', 'self', 'kw'))}
        kwargs.update(kw)
        super().__init__(**kwargs)


# noinspection PyRedeclaration
class HyperlinkedRelatedField(UUIDMixIn, ActionMixin, RenderToTableMixin, relations.HyperlinkedRelatedField):

    def __init__(self, view_name=None, read_only=False, write_only=False, required=None, default=fields.empty,
                 initial=fields.empty, source=None, label=None, help_text=None, style=None, error_messages=None,
                 validators=None, allow_null=False, uuid: UUID=None, **kw):
        kwargs = {k: v for k, v in locals().items() if not k.startswith(('__', 'self', 'kw'))}
        kwargs.update(kw)
        super().__init__(**kwargs)


# noinspection PyRedeclaration
class HyperlinkedIdentityField(UUIDMixIn, ActionMixin, RenderToTableMixin, relations.HyperlinkedIdentityField):

    def __init__(self, view_name=None, read_only=False, write_only=False, required=None, default=fields.empty,
                 initial=fields.empty, source=None, label=None, help_text=None, style=None, error_messages=None,
                 validators=None, allow_null=False, uuid: UUID=None, **kw):
        kwargs = {k: v for k, v in locals().items() if not k.startswith(('__', 'self', 'kw'))}
        kwargs.update(kw)
        super().__init__(**kwargs)


# noinspection PyRedeclaration
class SlugRelatedField(UUIDMixIn, ActionMixin, RenderToTableMixin, relations.SlugRelatedField):

    def __init__(self, slug_field=None, read_only=False, write_only=False, required=None, default=fields.empty,
                 initial=fields.empty, source=None, label=None, help_text=None, style=None, error_messages=None,
                 validators=None, allow_null=False, uuid: UUID=None, **kw):
        kwargs = {k: v for k, v in locals().items() if not k.startswith(('__', 'self', 'kw'))}
        kwargs.update(kw)
        super().__init__(**kwargs)
