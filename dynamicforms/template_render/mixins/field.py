from enum import auto
from typing import Any, Dict, Optional

from rest_framework.fields import Field

from dynamicforms.mixins.field_render import FieldRenderMixin

from .base import ViewModeBase
from .render_mode_enum import ViewModeEnum


class ViewModeField(ViewModeBase):
    """
    Binds the field definition from serializer to data for rendering
    """

    bound_value = None
    bound_value_row = None

    class ViewMode(ViewModeEnum):
        FORM = auto()  # Render to form field
        TABLE_DATA = auto()  # Render to table td
        TABLE_HEADER = auto()  # Render field label to table th

    def __init__(
        self,
        view_mode: "ViewModeField.ViewMode",
        field: FieldRenderMixin,
        value: Optional[Any] = None,
        value_row: Optional[Dict[Any, Any]] = None,
    ):
        """
        Will patch the field instance such that it will get this mixin mixed in.
        Optionally row and field values can also be provided for a one-off rendering

        :param field: serializer field instance
        :param value: field value in current data row
        :param value_row: current data row value
        """
        field.__class__ = type("ViewModeBoundField", (ViewModeField, field.__class__), {})
        self.set_bound_value(value, value_row)
        super().__init__(view_mode)

    def set_bound_value(self, value: Any, value_row: Dict[Any, Any]):
        self.bound_value = value
        self.bound_value_row = value_row

    def render_form(self: "_ViewModeBoundField"):
        """
        renders field's serialized value to HTML. Currently code only for performance reasons, we might support
        templating in the future

        :return: rendered value for form view
        """
        return self.bound_value

    def render_table(self: "_ViewModeBoundField"):
        """
        renders field's serialized value to HTML. Currently code only for performance reasons, we might support
        templating in the future

        :return: rendered value for table view
        """
        # TODO: Actually, the DRFTT.format_value() should be here and not in RenderMixin. Let's see if we can move it
        return self.bound_value


# noinspection PyAbstractClass
class _ViewModeBoundField(ViewModeField, Field):
    """
    Dummy class just for type hinting
    """

    pass
