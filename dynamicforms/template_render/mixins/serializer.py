from enum import auto
from typing import Any, Dict
from rest_framework.serializers import ListSerializer, Serializer

from dynamicforms.mixins import DisplayMode, RenderMixin
from .base import ViewModeBase
from .render_mode_enum import ViewModeEnum
from .serializer_render_fields import SerializerRenderFields
from .util import convert_to_json_if

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
    def is_rendering_as_table(self):
        """
        Overrides RenderMixin's implementation
        :return:
        """
        return self.view_mode in (ViewModeSerializer.ViewMode.TABLE_ROW, ViewModeSerializer.ViewMode.TABLE_HEAD)

    @property
    def render_fields(self: '_ViewModeBoundSerializer'):
        this = self

        class BoundSerializerRenderFields(SerializerRenderFields):

            @property
            def fields(self):
                # actions = self.actions.renderable_actions(self)
                # if any(action.position == "rowstart" for action in actions):
                #     yield fakefield(rowstart)

                for f in this.fields.values():
                    if f.display_table != DisplayMode.SUPPRESS:
                        yield f

                # if any(action.position == "rowend" for action in actions):
                #     yield fakefield(rowend)

        return BoundSerializerRenderFields()

    def component_params(self: '_ViewModeBoundSerializer', output_json: bool=True):
        params = {
            'guid': self.uuid,
            'columns': self.render_fields.columns.as_field_def(),  # todo: we need a self.setviewmode(header_row)
            'row-properties': self.render_fields.properties.as_name(),
            'record': None if self.parent else self.data
        }
        return convert_to_json_if(params, output_json)


# noinspection PyAbstractClass
class _ViewModeBoundSerializer(ViewModeSerializer, RenderMixin, Serializer):
    """
    Dummy class just for type hinting
    """
    class FakeActionsList(list):
        @staticmethod
        def renderable_actions(self, _unused):
            return self

    actions = FakeActionsList()
