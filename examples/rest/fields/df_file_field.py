import glob
import os
import pathlib
from typing import Optional

from django.core.files.uploadedfile import InMemoryUploadedFile
from django.utils.safestring import mark_safe
from rest_framework.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _

from dynamicforms.fields import FileField
from dynamicforms.preupload_files import preuploaded_fs, UPLOADED_FILE_NAME_UUID_SEPARATOR


class DfFileField(FileField):
    def to_representation(self, value, row_data=None):
        if not value:
            return ""
        link = mark_safe(
            '<a href="#" onclick=\'dynamicforms.stopEventPropagation(event); window.open("%s", "_blank")\'>%s</a>' % (
                value.url, os.path.basename(value.url)))
        if self.is_rendering_to_list:
            return link
        self.help_text = "Existing file: %s " % link
        return ""


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
        file: Optional[str] = next(iter(glob.glob(f'{preuploaded_fs.location}/*{data}*')), None)
        if not file and self.parent.instance.file:
            return data
        file_object = pathlib.Path(file)
        file_pointer = open(file, 'rb')
        return InMemoryUploadedFile(
            file=file_pointer,
            field_name=self.field_name,
            name=f'{file_object.stem.split(UPLOADED_FILE_NAME_UUID_SEPARATOR)[0]}{file_object.suffix}',
            content_type=None,
            size=len(file_pointer.read()), charset=None, content_type_extra=None
        )
