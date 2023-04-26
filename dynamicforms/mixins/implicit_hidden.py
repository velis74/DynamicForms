from .field_render import DisplayMode, FieldRenderMixin


class HiddenFieldMixin(FieldRenderMixin):
    def __init__(self, *args, **kwargs):
        kwargs.setdefault("display_table", DisplayMode.SUPPRESS)
        super().__init__(*args, **kwargs)
