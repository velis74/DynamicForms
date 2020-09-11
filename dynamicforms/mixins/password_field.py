class PasswordFieldMixin(object):

    def __init__(self, *args, password_field=False, **kwargs):
        super().__init__(*args, **kwargs)
        self.password_field = password_field or False

    def to_representation(self, value, row_data):
        if self.password_field:
            self.display_table = 'DisplayMode.SUPRESS'
        return super().to_representation(value, row_data)
