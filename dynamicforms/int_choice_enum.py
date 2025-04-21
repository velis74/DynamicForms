from enum import IntEnum


class IconisedString(str):
    def __new__(cls, value: str, icon: str = None, data: dict = None):
        obj = str.__new__(cls, value)
        obj.icon = icon
        obj.data = data
        return obj

class IntChoiceEnum(IntEnum):
    def __new__(cls, *args, **kwargs):
        obj = int.__new__(cls, args[0])
        obj._value_ = args[0]
        return obj

    # ignore the first param since it's already set by new
    def __init__(self, _: str, description: str = None, icon: str = None, data: dict = None):
        self._description_ = description
        self._icon_ = icon
        self._data_ = data

    description = property(lambda self: self._description_)
    icon = property(lambda self: self._icon_)
    data = property(lambda self: self._data_)

    @classmethod
    def get_choices_tuple(cls):
        return tuple((item.value, IconisedString(str(item.description), item.icon, item.data)) for item in cls)

    @classmethod
    def get_df_tuple(cls):
        return tuple(
            (item.value, item.description, item.icon) if item.icon is not None else (item.value, item.description)
            for item in cls
        )

    @classmethod
    def has_value(cls, value):
        return value in cls.__members__.values()
