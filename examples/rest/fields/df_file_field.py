import os

from django.utils.safestring import mark_safe

from dynamicforms_legacy.fields import FileField


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
