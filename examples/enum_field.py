from dynamicforms import fields

# TODO: #821 - Perhaps standard ChoiceField should support enums out-of-the-box?
#  e.g. if choices was an enum, it would resolve it into actual choices as well as support to_representation


class EnumField(fields.ChoiceField):
    def __init__(self, enum_type, *args, **kwds):
        kwds["choices"] = tuple([(member.value, member.name) for member in enum_type])
        super().__init__(*args, **kwds)
        self.enum_type = enum_type

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
