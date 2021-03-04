"""
What DynamicForms is about: ability to render a Serializer directly in Django template --> HTML
This module allows for it. It defines __str__ method on Serializer, ListSerializer and Field instances to render to HTML
"""
from enum import auto, Enum
from typing import Any, List, Dict, Optional

from rest_framework.fields import Field
from rest_framework.serializers import Serializer, ListSerializer

from .render import RenderMixin


class ViewModeEnum(Enum):
    # noinspection PyMethodParameters
    def _generate_next_value_(name, start, count, last_values):
        # We use this construct to obtain value same as name
        return name


class ViewModeBase(object):
    view_mode = None

    def set_view_mode(self, view_mode: 'ViewModeField.ViewMode'):
        self.view_mode = view_mode

    def set_bound_value(self, *args):
        """
        Used to set the bound value. However, implementation is class-specific, so we only declare this so that
        implementations are checked to contain the method
        """
        raise NotImplementedError()

    def render(self: '_ViewModeBoundField'):
        view_mode_name = f'render_{self.view_mode.name.lower()}'
        render_func = getattr(self, view_mode_name, None)
        if render_func is None:
            raise NotImplementedError(
                f'ViewMode object {self.__class__.__name__}{(" " + self.label) if self.label else ""} has view_mode '
                f'set to {self.view_mode.name}, but doesn\'t handle rendering for it'
            )
        return render_func()

    def __str__(self):
        return self.render()


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

    def __init__(self, view_mode: 'ViewModeField.ViewMode', field: RenderMixin, value: Optional[Any] = None,
                 value_row: Optional[Dict[Any, Any]] = None):
        """
        Will patch the field instance such that it will get this mixin mixed in.
        Optionally row and field values can also be provided for a one-off rendering

        :param field: serializer field instance
        :param value: field value in current data row
        :param value_row: current data row value
        """
        field.__class__ = type('ViewModeBoundField', (ViewModeField, field.__class__), {})
        self.set_bound_value(value, value_row)
        super().__init__(view_mode)

    def set_bound_value(self, value: Any, value_row: Dict[Any, Any]):
        self.bound_value = value
        self.bound_value_row = value_row

    def render_form(self: '_ViewModeBoundField'):
        """
        renders field's serialized value to HTML. Currently code only for performance reasons, we might support
        templating in the future

        :return: rendered value for form view
        """
        return self.bound_value

    def render_table(self: '_ViewModeBoundField'):
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


class ViewModeSerializer(ViewModeBase):
    """
    This one is actually a mixin, not a monkey-patch like the other two
    """
    bound_value = None

    class ViewMode(ViewModeEnum):
        FORM = auto()  # Render to form field
        TABLE_ROW = auto()  # Render to table tr
        TABLE_HEAD = auto()  # Render to table header

    def __init__(self, *args, view_mode: 'ViewModeSerializer.ViewMode' = None,
                 view_mode_list: 'ViewModeListSerializer.ViewMode' = None,
                 **kwds
                 ):
        super().__init__(*args, **kwds)
        self.set_view_mode(view_mode)
        self.view_mode_list = view_mode_list

    def __new__(cls, *args, **kwargs):
        view_mode_list = kwargs.pop('view_mode_list', None)
        res = super().__new__(cls, *args, **kwargs)
        if isinstance(res, ListSerializer):
            res = ViewModeListSerializer.mixin_to_serializer(view_mode_list, res)
        return res

    def set_bound_value(self, value: Dict[Any, Any]):
        self.bound_value = value


# noinspection PyAbstractClass
class _ViewModeBoundSerializer(ViewModeSerializer, Serializer):
    """
    Dummy class just for type hinting
    """
    pass


class ViewModeListSerializer(ViewModeBase):
    bound_value = None

    class ViewMode(ViewModeEnum):
        TABLE = auto()  # Render to full table with header, filter, rows

    # noinspection PySuperArguments,PyUnresolvedReferences
    @staticmethod
    def mixin_to_serializer(view_mode: 'ViewModeSerializer.ViewMode', serializer: ListSerializer,
                            value: Optional[List[Dict]] = None):
        serializer.__class__ = type(
            'ViewMode' + serializer.child.__class__.__name__, (ViewModeListSerializer, serializer.__class__), {}
        )
        super(ViewModeListSerializer, serializer).set_view_mode(view_mode)
        serializer.set_bound_value(value)
        return serializer

    def set_bound_value(self, value: List[Dict]):
        self.bound_value = value

    def render_table(self: '_ViewModeBoundListSerializer'):
        return 'juhuhu'


# noinspection PyAbstractClass
class _ViewModeBoundListSerializer(ViewModeSerializer, ListSerializer):
    """
    Dummy class just for type hinting
    """
    pass
