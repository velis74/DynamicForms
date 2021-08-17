from typing import Dict, List, Optional, Tuple, TYPE_CHECKING, Union

from dynamicforms.fields import DFField, DisplayMode

if TYPE_CHECKING:
    from dynamicforms.serializers import Serializer


class Field(object):
    def __init__(self, field_name: str, field_def: Optional[DFField] = None, render_format: Optional[str] = None):
        self.field_name = field_name
        self.field_def = field_def
        self.render_format = render_format

    def bind_field(self, field_name: str, field) -> bool:
        res = self.field_name == field_name
        if res and not self.field_def:
            self.field_def = field
        return res

    def as_component_def(self):
        fdef = self.field_def  # type: DFField
        res = fdef.as_component_def()
        res.update(dict(name=self.field_name))
        if self.render_format:
            res['render_format'] = self.render_format
        return res


class Column(object):
    def __init__(self, field: Union[Tuple[str, DFField], Field, str, None], width_classes: Optional[str] = None):
        if isinstance(field, tuple):
            self.field = Field(field[0], field[1])
        elif isinstance(field, str):
            self.field = Field(field, None)
        elif isinstance(field, Field):
            self.field = field
        else:
            raise NotImplementedError(f'Unknown field type {field.__class__.__name__}')
        self.width_classes = width_classes or ''

    def bind_field(self, field_name: str, field) -> bool:
        return self.field.bind_field(field_name, field)

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
            elif isinstance(column, str):
                self.columns.append(Column(Field(column)))
            elif isinstance(column, Field):
                self.columns.append(Column(column))
            elif isinstance(column, Column):
                self.columns.append(column)
            else:
                raise NotImplementedError(f'Unknown column type {column.__class__.__name__}')

    def bind_field(self, field_name: str, field) -> bool:
        # list() is necessary so that all rows evaluate
        return any(list(map(lambda column: column.bind_field(field_name, field), self.columns)))

    def as_component_def(self) -> List[Dict]:
        return [col.as_component_def() for col in self.columns]


class Layout(object):
    def __init__(self, *rows: Row, columns: int = 1, size: str = ''):
        """
        Creates layout definition
        :param rows: layout rows containing columns & fields
        :param columns: for all fields not added in layout manually, add them in n-column layout
        :param size: 'small', 'large' or ''
        """
        self.rows = rows or []
        self.columns = columns
        self.size = size

    def bind_field(self, field_name: str, field_def) -> bool:
        # list() is necessary so that all rows evaluate
        return any(list(map(lambda row: row.bind_field(field_name, field_def), self.rows)))

    def as_component_def(self, serializer: Optional['Serializer']) -> Dict:
        if serializer:
            for field_name, field in serializer.fields.items():
                self.bind_field(field_name, field)

        res = dict(rows=[row.as_component_def() for row in self.rows])
        if self.size:
            res['size'] = self.size

        if serializer:
            default_layout = Layout()
            row = []
            row_num = 0
            for field_name, field in serializer.fields.items():
                if not self.bind_field(field_name, field) and field.display_form != DisplayMode.SUPPRESS:
                    row.append((field_name, field))
                    if field.display_form == DisplayMode.FULL:
                        row_num += 1
                    if row_num >= self.columns:
                        default_layout.rows.append(Row(*row))
                        row, row_num = [], 0
            if row:
                default_layout.rows.append(Row(*row))
            res['rows'] += default_layout.as_component_def(None)['rows']
            res['actions'] = serializer.render_actions.form.as_action_def()
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
