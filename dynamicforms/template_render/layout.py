from typing import Dict, List, Optional, Tuple, TYPE_CHECKING, Union

from dynamicforms.fields import DFField, DisplayMode

if TYPE_CHECKING:
    from dynamicforms.serializers import Serializer


class Field(object):
    def __init__(self, field_name: str, render_format: Optional[str] = None):
        self.field_name = field_name
        self.render_format = render_format

    def field_def(self, serializer: 'Serializer') -> DFField:
        return serializer.fields[self.field_name]

    def as_component_def(self, serializer: 'Serializer'):
        res = self.field_def(serializer).as_component_def()
        res.update(dict(name=self.field_name))
        if self.render_format:
            res['render_format'] = self.render_format
        return res


class Column(object):
    def __init__(self, field: Union[Tuple[str, DFField], Field, str, None], width_classes: Optional[str] = None):
        if isinstance(field, str):
            self.field = Field(field)
        elif isinstance(field, Field):
            self.field = field
        else:
            raise NotImplementedError(f'Unknown field type {field.__class__.__name__}')
        self.width_classes = width_classes or ''

    def _get_laid_fields(self):
        return {self.field.field_name}

    def as_component_def(self, serializer: 'Serializer') -> Dict:
        res = dict(type='column', field=self.field.as_component_def(serializer))
        if self.width_classes:
            res['width_classes'] = self.width_classes
        return res


class Row(object):
    def __init__(self, *columns, component: str = None):
        self.component = component or 'DFFormRow'
        self.columns = []  # type: List[Column]
        for column in columns:
            if isinstance(column, str):
                self.columns.append(Column(Field(column)))
            elif isinstance(column, Field):
                self.columns.append(Column(column))
            elif isinstance(column, Column):
                self.columns.append(column)
            else:
                raise NotImplementedError(f'Unknown column type {column.__class__.__name__}')

    def _get_laid_fields(self):
        return set().union(*(col._get_laid_fields() for col in self.columns))

    def as_component_def(self, serializer: 'Serializer') -> dict:
        return dict(component=self.component, columns=[col.as_component_def(serializer) for col in self.columns])


class Layout(object):
    def __init__(self, *rows: Row, columns: int = 1, size: str = '', header_classes: str = ''):
        """
        Creates layout definition
        :param rows: layout rows containing columns & fields
        :param columns: for all fields not added in layout manually, add them in n-column layout
        :param size: 'small', 'large' or ''
        :param header_classes: 'bg-info', ..., or ''
        """
        self.rows = rows or []  # type: List[Row]
        self.columns = columns
        self.size = size
        self.header_classes = header_classes

    def _get_laid_fields(self):
        return set().union(*(row._get_laid_fields() for row in self.rows))

    def as_component_def(self, serializer: 'Serializer', used_fields: set=None) -> Dict:
        assert serializer is not None
        res = dict(rows=[row.as_component_def(serializer) for row in self.rows])
        used_fields = (used_fields or set()).union(self._get_laid_fields())
        if self.size:
            res['size'] = self.size
        if self.header_classes:
            res['header_classes'] = self.header_classes

        # add any non-declared fields and append them to the end of the layout
        # if no layout is specified in serializer Meta, this will generate default single-column layout
        default_layout = Layout()
        row = []
        row_num = 0
        for field_name, field in serializer.fields.items():
            if field_name not in used_fields and field.display_form != DisplayMode.SUPPRESS:
                used_fields.add(field_name)
                row.append(field_name)
                if field.display_form == DisplayMode.FULL:
                    row_num += 1
                if row_num >= self.columns:
                    default_layout.rows.append(Row(*row))
                    row, row_num = [], 0
        if row:
            default_layout.rows.append(Row(*row))
        if default_layout.rows:
            res['rows'] += default_layout.as_component_def(serializer, used_fields)['rows']
        res['actions'] = serializer.render_actions.form.as_action_def()
        return res


class Group(Column):
    def __init__(self, field: Union[str, Field, None], title, sub_layout: Layout,
                 width_classes: Optional[str] = None, footer: Optional[str] = None):
        super().__init__(field, width_classes)
        self.title = title
        self.layout = sub_layout
        self.footer = footer

    def _get_laid_fields(self):
        return self.layout._get_laid_fields()

    def as_component_def(self, serializer: 'Serializer') -> Dict:
        res = super().as_component_def(serializer)
        res.update(
            dict(type='group', title=self.title, footer=self.footer, layout=self.layout.as_component_def(serializer))
        )
        return res
