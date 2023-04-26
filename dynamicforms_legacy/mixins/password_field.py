class PasswordFieldMixin(object):
    def __init__(self, *args, password_field=False, **kwargs):
        super().__init__(*args, **kwargs)
        self.password_field = password_field

    def set_password_field(self, value):
        self._password_field = value
        if value:
            self.display_table = "DisplayMode.SUPRESS"
            self.style.update(input_type="password")
        else:
            try:
                self.style["input_type"]
                self.style.update(input_type="text")
                self.display_table = "DisplayMode.FULL"
            except:
                pass

    password_field = property(lambda self: self._password_field, set_password_field)
