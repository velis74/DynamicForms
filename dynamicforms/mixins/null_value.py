from rest_framework.fields import IntegerField


class NullValueMixin(object):
    def to_internal_value(self, data):
        if data == "" and self.allow_null:
            self.validators = []
            return None
        return super().to_internal_value(data)

    def to_representation(self, value, row_data=None):
        if value is None and self.allow_null and not isinstance(self, IntegerField):
            value = ""

        return super().to_representation(value, row_data)
