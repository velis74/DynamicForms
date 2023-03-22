from dynamicforms import fields


class EnumField(fields.ChoiceField):

    def __init__(self, enum_type, *args, **kwds):
        kwds['choices'] = tuple([(member.value, member.name) for member in enum_type])
        super().__init__(*args, **kwds)
        self.enum_type = enum_type

    def to_internal_value(self, data):
        return self.enum_type(data)

    def to_representation(self, value, row_data=None):
        return value.value if isinstance(value, self.enum_type) else value
