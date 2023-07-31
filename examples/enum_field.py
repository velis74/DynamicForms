from dynamicforms import fields


class EnumField(fields.ChoiceField):
    def __init__(self, enum_type, *args, **kwds):
        kwds["choices"] = tuple([(member.value, member.name) for member in enum_type])
        super().__init__(*args, **kwds)
        self.enum_type = enum_type

    def to_internal_value(self, data):
        return self.enum_type(data[0] if isinstance(data, list) else data)

    def to_representation(self, value, row_data=None):
        if isinstance(value, self.enum_type):
            value = value.value
        return super().to_representation(value, row_data)

    def render_to_table(self, value, row_data):
        try:
            if not isinstance(value, self.enum_type):
                value = self.enum_type(value)
            return value.name
        except ValueError:
            pass  # If the value is not in the enum, just skip to default rendering
        return value
