from .render import DisplayMode


class SingleChoiceMixin:
    def __init__(self, *args, single_choice_hide=False, **kwargs):
        super().__init__(*args, **kwargs)
        self.single_choice_hide = single_choice_hide

    def to_internal_value(self, data):
        if self.single_choice_hide and len(self.choices) == 1:
            data = list(self.choices)[0]
        elif self.single_choice_hide and len(self.choices) < 1:
            data = None
        return super().to_internal_value(data)

    def set_single_choice_hide(self, value):
        self._single_choice_hide = value
        if value and len(self.choices) <= 1:
            self.display_form = DisplayMode.HIDDEN

    single_choice_hide = property(lambda self: self._single_choice_hide, set_single_choice_hide)
