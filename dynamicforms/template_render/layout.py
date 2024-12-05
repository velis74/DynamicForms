import uuid

from typing import Dict, List, Optional, Tuple, TYPE_CHECKING, Union

from rest_framework.serializers import Serializer as DRFSerializer

from dynamicforms.fields import DFField, DisplayMode

if TYPE_CHECKING:
    from dynamicforms.serializers import Serializer


class Field(object):
    def __init__(self, field_name: str, render_format: Optional[str] = None):
        self.field_name = field_name
        self.render_format = render_format

    def clone(self):
        return Field(self.field_name, self.render_format)

    def field_def(self, serializer: "Serializer") -> Union[DFField, DRFSerializer]:
        return serializer.fields[self.field_name]

    def as_component_def(self, serializer: "Serializer", fields: Dict):
        field = self.field_def(serializer).as_component_def()

        field["name"] = self.field_name
        if self.render_format:
            field["render_format"] = self.render_format
        fields[self.field_name] = field
        return field["name"]


class Column(object):
    def __init__(self, field: Union[Tuple[str, DFField], Field, str, None], width_classes: Optional[str] = None):
        if isinstance(field, str):
            self.field = Field(field)
        elif isinstance(field, Field):
            self.field = field
        elif field is None and isinstance(self, Group):
            # a Group might not have a field attached to it
            self.field = field
        else:
            raise NotImplementedError(f"Unknown field type {field.__class__.__name__}")
        self.width_classes = width_classes or ""
        # TODO: It was a lot more useful when bootstrap was the front-end framework and this basically allowed to
        #  specify how big a column was to be used. Needs to change to support the Vue / Vuetify components and
        #  their props now. task: https://app.clickup.com/t/86bzw1k8f

    def clone(self):
        return Column(field=self.field.clone() if self.field else None, width_classes=self.width_classes)

    def _get_laid_fields(self):
        return {self.field.field_name} if self.field is not None else set()

    def as_component_def(self, serializer: "Serializer", fields: Dict) -> Dict:
        fld_def = self.field.as_component_def(serializer, fields) if self.field is not None else dict()
        res = dict(type="column", field=fld_def)
        if self.width_classes:
            res["width_classes"] = self.width_classes
        return res


class Row(object):
    def __init__(self, *columns: Union[Column, Field, str], component: str = None):
        self.component = component or "FormRow"
        self.columns: List[Column] = []
        for column in columns:
            if isinstance(column, str):
                self.columns.append(Column(Field(column)))
            elif isinstance(column, Field):
                self.columns.append(Column(column))
            elif isinstance(column, Column):
                self.columns.append(column)
            else:
                raise NotImplementedError(f"Unknown column type {column.__class__.__name__}")

    def clone(self):
        return Row(*[col.clone() for col in self.columns], component=self.component)

    def _get_laid_fields(self):
        return set().union(*(col._get_laid_fields() for col in self.columns))

    def as_component_def(self, serializer: "Serializer", fields: Dict) -> dict:
        return dict(
            component=self.component, columns=[col.as_component_def(serializer, fields) for col in self.columns]
        )


class Layout(object):
    def __init__(
        self,
        *rows: Row,
        component_name: str = "df-form-layout",
        columns: int = 1,
        size: str = "",
        header_classes: str = "",
        auto_add_fields: bool = True,
    ):
        """
        Creates layout definition
        :param rows: layout rows containing columns & fields
        :param columns: for all fields not added in layout manually, add them in n-column layout
        :param size: 'small', 'large' or ''
        :param header_classes: 'bg-info', ..., or ''
        """
        self.rows: List[Row] = list(rows) or []
        self.columns = columns
        self.size = size
        self.header_classes = header_classes
        self.component_name = component_name
        self.auto_add_fields = auto_add_fields

    def clone(self):
        return Layout(
            *[row.clone() for row in self.rows],
            component_name=self.component_name,
            columns=self.columns,
            size=self.size,
            header_classes=self.header_classes,
            auto_add_fields=self.auto_add_fields
        )

    def append_after_row(self, field_name: Optional[str], *rows: Row):
        """Adds new rows after the row with specified field. if field_name is None, inserts new rows at beginning"""
        if field_name is None:
            self.rows[0:0] = rows
            return
        for i, row in enumerate(self.rows):
            for column in row.columns:
                if column.field and column.field.field_name == field_name:
                    self.rows[i + 1:i + 1] = rows
                    return
        raise ValueError(f"Field {field_name} not found in the layout")

    def _get_laid_fields(self):
        return set().union(*(row._get_laid_fields() for row in self.rows))

    def as_component_def(self, serializer: "Serializer", fields: Dict = None, used_fields: set = None) -> Dict:
        assert serializer is not None
        fields = fields if fields is not None else dict()
        res = dict(rows=[row.as_component_def(serializer, fields) for row in self.rows])
        res["fields"] = fields
        used_fields = (used_fields or set()).union(self._get_laid_fields())
        if self.size:
            res["size"] = self.size
        if self.header_classes:
            res["header_classes"] = self.header_classes

        if self.auto_add_fields:
            # add any non-declared fields and append them to the end of the layout
            # if no layout is specified in serializer Meta, this will generate default single-column layout
            default_layout = Layout()
            row = []
            row_num = 0
            for field_name, field in serializer.fields.items():
                if field_name not in used_fields and field.display_form != DisplayMode.SUPPRESS:
                    used_fields.add(field_name)
                    row.append(
                        Group(field_name)  # nested Serializer or ListSerializer
                        if isinstance(field, DRFSerializer)
                        else field_name  # "just" a standard field
                    )
                    if field.display_form == DisplayMode.FULL:
                        row_num += 1
                    if row_num >= self.columns:
                        default_layout.rows.append(Row(*row))
                        row, row_num = [], 0
            if row:
                default_layout.rows.append(Row(*row))
            if default_layout.rows:
                res["rows"] += default_layout.as_component_def(serializer, fields, used_fields)["rows"]

        res["component_name"] = self.component_name
        return res


class Group(Column):
    def __init__(
        self,
        field: Union[str, Field, None],
        title: str = None,
        sub_layout: Layout = None,
        width_classes: Optional[str] = None,
        footer: Optional[str] = None,
    ):
        super().__init__(field, width_classes)
        self.title = title
        self.layout = sub_layout
        self.footer = footer

    def clone(self):
        return Group(
            field=self.field.clone() if self.field else None,
            title=self.title,
            sub_layout=self.layout.clone() if self.layout else None,
            width_classes=self.width_classes,
            footer=self.footer
        )

    def _get_laid_fields(self):
        if self.field is None:
            return self.layout._get_laid_fields()
        return super()._get_laid_fields()

    def as_component_def(self, serializer: "Serializer", fields: Dict) -> Dict:
        res = super().as_component_def(serializer, fields)
        assert self.field or self.layout
        sub_serializer = self.field.field_def(serializer) if self.field else None  # type: Serializer
        layout = self.layout or sub_serializer.layout
        res.update(
            type="group",
            footer=self.footer,
            title=self.title or sub_serializer.label,
            uuid=sub_serializer.uuid if sub_serializer else uuid.uuid4(),
            layout=layout.as_component_def(sub_serializer if sub_serializer else serializer),
        )
        return res
