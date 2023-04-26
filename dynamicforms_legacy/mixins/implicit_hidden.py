from .render import DisplayMode, RenderMixin


class HiddenFieldMixin(RenderMixin):
    def __init__(self, *args, **kwargs):
        kwargs.setdefault("display_table", DisplayMode.SUPPRESS)
        super().__init__(*args, **kwargs)
