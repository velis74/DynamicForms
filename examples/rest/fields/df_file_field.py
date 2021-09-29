import os

from django.utils.safestring import mark_safe
from rest_framework.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _

from dynamicforms.fields import FileField


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


class DfPreloadedFileField(DfFileField):
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

    def to_internal_value(self, data):
        if not isinstance(data, str):
            raise ValidationError(_('File identifier should be string'))
        file_size = len(data)
        if not self.allow_empty_file and not file_size:
            self.fail('empty')
        return data
