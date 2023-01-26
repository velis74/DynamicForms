from enum import Enum


class ViewModeEnum(Enum):
    # noinspection PyMethodParameters
    def _generate_next_value_(name, start, count, last_values):
        # We use this construct to obtain value same as name
        return name
