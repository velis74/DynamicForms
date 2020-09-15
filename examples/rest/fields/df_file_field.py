import os

from django.utils.safestring import mark_safe

from dynamicforms.fields import FileField


class DfFileField(FileField):
    def to_representation(self, value, row_data=None) -> str:
        if not value:
            return ""
        if self.is_rendering_to_list:
            return mark_safe(
                '<a href="#" onclick=\'event.stopPropagation(); window.open("%s", "_blank")\'>%s</a>' % (
                    value.url, os.path.basename(value.url)))
        self.help_text = "Existing file: %s " % os.path.basename(value.url)
        return ""