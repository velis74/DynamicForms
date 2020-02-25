from dynamicforms import fields


class NameTestField(fields.CharField):

    def to_representation(self, value):
        if not value.pk:
            return None
        return value.name

    def to_internal_value(self, data):
        return {
            'name': super().to_internal_value(data)
        }
