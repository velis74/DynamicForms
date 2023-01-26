from typing import Optional, Union


class FieldHelpTextMixin(object):
    """
    Redefines help_text property such that we can set help text for api docs and form help text
    """

    def __init__(self, *args, help_text: Union[str, dict, None] = None, help_text_form: Optional[str] = None,
                 **kwargs) -> None:
        super().__init__(*args, help_text=help_text, **kwargs)
        self.help_text = help_text
        if help_text_form or not isinstance(help_text, dict):
            self._help_text_form = help_text_form or self.help_text

    def get_help_text(self):
        return self._help_text

    def set_help_text(self, value):
        if isinstance(value, dict):
            self._help_text = value.get('doc', None)
            self._help_text_form = value.get('form', None)
        else:
            self._help_text = value
            self._help_text_form = getattr(self, '_help_text_form', None) or value

    def get_help_text_form(self):
        return self._help_text_form

    def set_help_text_form(self, value):
        if isinstance(value, dict):
            self._help_text = value.get('form', None)
        else:
            self._help_text_form = value

    help_text = property(get_help_text, set_help_text)
    help_text_form = property(get_help_text_form, set_help_text_form)
