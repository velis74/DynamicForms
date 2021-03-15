from enum import auto
from typing import Any, Dict

from rest_framework.serializers import ListSerializer, Serializer

from dynamicforms.mixins import DisplayMode
from .base import ViewModeBase
from .render_mode_enum import ViewModeEnum

# noinspection PyUnreachableCode
if False:
    from .listserializer import ViewModeListSerializer


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
        from .listserializer import ViewModeListSerializer

        view_mode_list = kwargs.pop('view_mode_list', None)
        res = super().__new__(cls, *args, **kwargs)
        if isinstance(res, ListSerializer):
            res = ViewModeListSerializer.mixin_to_serializer(view_mode_list, res)
        return res

    def set_bound_value(self, value: Dict[Any, Any]):
        self.bound_value = value

    @property
    def render_fields(self: '_ViewModeBoundSerializer'):
        # actions = self.actions.renderable_actions(self)
        # if any(action.position == "rowstart" for action in actions):
        #     yield fakefield(rowstart)

        for f in self.fields.values():
            if f.display_table == DisplayMode.FULL:
                yield f

        # if any(action.position == "rowend" for action in actions):
        #     yield fakefield(rowend)


# noinspection PyAbstractClass
class _ViewModeBoundSerializer(ViewModeSerializer, Serializer):
    """
    Dummy class just for type hinting
    """
    class FakeActionsList(list):
        @staticmethod
        def renderable_actions(self, _unused):
            return self

    actions = FakeActionsList()
