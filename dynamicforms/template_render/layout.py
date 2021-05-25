from typing import Dict, List, Optional, TYPE_CHECKING, Union, Tuple
from rest_framework.fields import Field as DRFField
from dynamicforms.mixins.render import DisplayMode

if TYPE_CHECKING:
    from dynamicforms.serializers import Serializer


class Field(object):
    def __init__(self, field_name: str, field_def: DRFField, render_format: Optional[str] = None):
        self.field_name = field_name
        self.field_def = field_def
        self.render_format = render_format

    def is_field(self, field_name: str) -> bool:
        return self.field_name == field_name

    def as_component_def(self):
        fdef = self.field_def
        res = dict(
            field_name=self.field_name, uuid=fdef.uuid, display=fdef.display_form,
            alignment=fdef.alignment.name.lower(), render_widget=fdef.render_widget, help_text=fdef.help_text,
            label=fdef.label,
        )
        if self.render_format:
            res['render_format'] = self.render_format
        return res


class Column(object):
    def __init__(self, field: Union[Tuple[str, DRFField], Field, None], width_classes: Optional[str] = None):
        if isinstance(field, tuple):
            self.field = Field(field[0], field[1])
        elif isinstance(field, Field):
            self.field = field
        else:
            raise NotImplementedError(f'Unknown field type {field.__class__.__name__}')
        self.width_classes = width_classes or ''

    def has_field(self, field_name: str) -> bool:
        return self.field.is_field(field_name)

    def as_component_def(self) -> Dict:
        res = dict(type='column', field=self.field.as_component_def())
        if self.width_classes:
            res['width_classes'] = self.width_classes
        return res


class Row(object):
    def __init__(self, *columns):
        self.columns = []
        for column in columns:
            if isinstance(column, tuple):
                self.columns.append(Column(Field(*column)))
            elif isinstance(column, Field):
                self.columns.append(Column(column))
            elif isinstance(column, Column):
                self.columns.append(column)
            else:
                raise NotImplementedError(f'Unknown column type {column.__class__.__name__}')

    def has_field(self, field_name: str) -> bool:
        return any(map(lambda column: column.has_field(field_name), self.columns))

    def as_component_def(self) -> List[Dict]:
        return [col.as_component_def() for col in self.columns]


class Layout(object):
    def __init__(self, *rows: List[Row]):
        self.rows = [Row(row) for row in rows]

    def has_field(self, field_name: str) -> bool:
        return any(map(lambda row: row.has_field(field_name), self.rows))

    def as_component_def(self, serializer: Optional['Serializer']) -> List[List[Dict]]:
        res = [row.as_component_def() for row in self.rows]
        if serializer:
            default_layout = Layout()
            for field_name, field in serializer.fields.items():
                if not self.has_field(field_name) and field.display_form != DisplayMode.SUPPRESS:
                    default_layout.rows.append(Row((field_name, field)))
            res += default_layout.as_component_def(None)
        return res


class Group(Column):
    def __init__(self, field: Union[str, Field, None], title, sub_layout: Layout,
                 width_classes: Optional[str] = None, footer: Optional[str] = None):
        super().__init__(field, width_classes)
        self.title = title
        self.layout = sub_layout
        self.footer = footer

    def as_component_def(self) -> Dict:
        res = super().as_component_def()
        res.update(
            dict(type='group', title=self.title, footer=self.footer, layout=self.layout.as_component_def(None))
        )
        return res
