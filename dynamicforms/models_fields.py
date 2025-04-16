from typing import Type

from django.db.models.fields import IntegerField

from dynamicforms.models_utils import IntChoiceEnum


class EnumChoiceField(IntegerField):
    def __init__(self, enum: Type[IntChoiceEnum], **kwargs):
        kwargs["choices"] = enum.get_choices_tuple()
        self._enum = enum
        super().__init__(**kwargs)

    def to_python(self, value):
        if value is None:
            return None
        if isinstance(value, self.enum):
            return value
        python_value = super().to_python(value)
        if python_value is None:
            return None
        return self.enum(python_value)

    def get_prep_value(self, value):
        if value is None:
            return None
        return value.value if isinstance(value, self.enum) else value

    def from_db_value(self, value, expression, connection):
        return self.to_python(value)

    @property
    def enum(self):
        return self._enum

    def deconstruct(self):
        name, path, args, kwargs = super().deconstruct()
        kwargs["enum"] = self.enum
        # Remove the choices from kwargs as they're derived from the enum
        if "choices" in kwargs:
            del kwargs["choices"]
        return name, path, args, kwargs
