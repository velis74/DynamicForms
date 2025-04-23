import sys

from typing import Type

from django.core import validators
from django.db.models.fields import IntegerField, PositiveIntegerField
from django.utils.functional import cached_property

from dynamicforms.int_choice_enum import IntChoiceEnum


def check_remove_choices():
    if "makemigrations" in sys.argv:  # or settings.CURRENT_TEST == "test_pending_migration":
        return True
    return False


class IntegerChoiceMigrationIgnoreField(IntegerField):
    # Prevent making migrations for every choice/version change
    # https://stackoverflow.com/a/51724865/9625282
    description = "Integer choices field that ignores changes of choices in migrations"

    def deconstruct(self):
        name, path, args, kwargs = super(IntegerChoiceMigrationIgnoreField, self).deconstruct()

        if check_remove_choices():
            kwargs.pop("choices", None)
        return name, path, args, kwargs


class EnumChoiceField(IntegerChoiceMigrationIgnoreField):
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


class ColorField(PositiveIntegerField):
    description = (
        "Field for storing colours, storing them as 32-bit integers, but representing them as html hex colour strings"
    )

    @cached_property
    def validators(self):
        # we are removing the minvalue and maxvalue validators as a hack to prevent DRF from adding those values
        # to ColorField constructor
        res = super().validators
        return list(
            filter(
                lambda v: not isinstance(v, (validators.MinValueValidator, validators.MaxValueValidator)),
                res,
            )
        )

    def from_db_value(self, value, expression, connection):
        if value is None:
            return value
        if value > 0xFFFFFF:
            # also the alpha channel
            return f"#{value:08x}"

        return f"#{value:06x}"

    def _input_to_int(self, value):
        if value is None:
            return value
        if isinstance(value, str) and value.startswith("#"):
            # Convert from #(aa)rrggbb or #(a)rgb to uint before storing to database
            hex_val = value[1:]
            if len(hex_val) <= 4:  # #(a)rgb -> (aa)rrggbb
                hex_val = "".join([c + c for c in hex_val])
            return int(hex_val, 16)
        return value

    def to_python(self, value):
        return self._input_to_int(value)

    def get_prep_value(self, value):
        return self._input_to_int(value)
