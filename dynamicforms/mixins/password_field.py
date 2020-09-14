class PasswordFieldMixin(object):

    def __init__(self, *args, password_field=False, **kwargs):
        super().__init__(*args, **kwargs)

        self.password_field = password_field or False

        if self.password_field:
            self.display_table = 'DisplayMode.SUPRESS'
            self.style.update(input_type='password')
