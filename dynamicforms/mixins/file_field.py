from typing import TYPE_CHECKING

from django.utils.translation import gettext_lazy as _

if TYPE_CHECKING:
    from rest_framework.fields import FileField


class FileFieldMixin(object):
    def __init__(self, **kwargs) -> None:
        super().__init__(**kwargs)
        # noinspection PyUnresolvedReferences
        self.style.setdefault("no_filter", True)

    def to_representation(self: "FileField", value, row_data=None):
        if value:
            return getattr(value, "url", None)
        return None

    def to_internal_value(self: "FileField", data):
        from django.core.files.base import ContentFile
        from rest_framework.exceptions import ValidationError

        from dynamicforms.preupload_files import get_cached_file

        if isinstance(data, str):  # dobimo guid
            cached_file = get_cached_file(data, self.context["request"].user.id or -1, True)
            if cached_file:
                # Naredimo django file iz cache podatkov
                return ContentFile(cached_file.content, name=cached_file.name)

            # Če datoteke ni v cache-u in imamo obstoječo vrednost na instanci, vrnemo obstoječo vrednost
            if self.parent.instance and getattr(self.parent.instance, self.field_name, None):
                return str(getattr(self.parent.instance, self.field_name))
            raise ValidationError(_("File not found in cache"))

        if not self.allow_empty_file and not data:
            self.fail("empty")

        return super().to_internal_value(data)

    def validate_empty_values(self: "FileField", data):
        """Override za boljše rokovanje z empty vrednostmi"""
        if data is None:
            if self.required:
                self.fail("required")
            return True, None

        if data == "" and self.allow_empty_file:
            return True, None

        return False, data
