from .render import DisplayMode


class FileFieldMixin(object):

    def to_representation(self, instance, row_data=None):
        if self.parent.is_filter:
            self.display = DisplayMode.INVISIBLE
        return super().to_representation(instance, row_data)
