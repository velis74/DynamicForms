import glob
import os
import pathlib
from typing import Optional

from django.core.files.uploadedfile import InMemoryUploadedFile
from django.utils.safestring import mark_safe
from django.utils.translation import gettext_lazy as _
from rest_framework.exceptions import ValidationError

from dynamicforms.fields import FileField
from dynamicforms.preupload_files import (
    preuploaded_fs, UPLOADED_FILE_NAME_TIMESTAMP_SEPARATOR, UPLOADED_FILE_NAME_UUID_SEPARATOR
)
from dynamicforms.settings import COMPONENT_DEF_RENDERER_FORMAT


class DfFileField(FileField):
    def to_representation(self, value, row_data=None):
        empty_value: Optional[str] = ''
        render_to_component_def_format: bool = self.context.get('format', '') == COMPONENT_DEF_RENDERER_FORMAT
        if render_to_component_def_format:
            empty_value = None
        if not value:
            return empty_value
        link = mark_safe(
            '<a href="#" onclick=\'dynamicforms.stopEventPropagation(event); window.open("%s", "_blank")\'>%s</a>' % (
                value.url, os.path.basename(value.url)))
        if self.is_rendering_to_list:
            return link if not render_to_component_def_format else value.url
        self.help_text = "Existing file: %s " % link
        return empty_value


class DfPreloadedFileField(FileField):

    def to_representation(self, value, row_data=None):
        if value:
            return getattr(value, 'url', None)
        return None

    def to_internal_value(self, data):
        if not isinstance(data, str):
            raise ValidationError(_('File identifier should be string'))
        file_size = len(data)
        if not self.allow_empty_file and not file_size:
            self.fail('empty')
        file: Optional[str] = next(iter(glob.glob(
            f'{preuploaded_fs.location}/*{UPLOADED_FILE_NAME_UUID_SEPARATOR}*{data}*{UPLOADED_FILE_NAME_TIMESTAMP_SEPARATOR}*')),
            None)
        if not file and self.parent.instance and getattr(self.parent.instance, self.field_name, None):
            return str(getattr(self.parent.instance, self.field_name))
        file_object = pathlib.Path(file)
        file_pointer = open(file, 'rb')
        return InMemoryUploadedFile(
            file=file_pointer,
            field_name=self.field_name,
            name=f'{file_object.stem.split(UPLOADED_FILE_NAME_UUID_SEPARATOR)[0]}{file_object.suffix}',
            content_type=None,
            size=len(file_pointer.read()), charset=None, content_type_extra=None
        )
