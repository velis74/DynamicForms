"""
Responsive Table Layouts

Allows for declaring ever narrower row layouts that will be used when target viewPort is too narrow to display
all columns in one row. When this is detected, a layout will be selected that can still fit in the given width.

when all layouts are too wide, the most narrow one will be chosen.

This file has a counterpart in responsive-layout.js
"""
from typing import List, Optional, TYPE_CHECKING, Union

if TYPE_CHECKING:
    from dynamicforms.serializers import Serializer


class ColumnRow:
    def __init__(self, columns: List[str]):
        assert all((isinstance(column, str) for column in columns))
        self.columns = columns

    def as_component_def(self, serializer: "Serializer"):
        return self.columns


class ColumnGroup:
    def __init__(self, rows: Union[str, List[Union[str, List[str]]]]):
        rows_list = [rows] if isinstance(rows, str) else rows
        self.rows = [ColumnRow(row) for row in rows_list]

    def as_component_def(self, serializer: "Serializer"):
        return [row.as_component_def(serializer) for row in self.rows]


class ResponsiveTableLayout:
    def __init__(self, *columns: Union[str, List], auto_add_non_listed_columns: bool = True):
        self.columns = [ColumnGroup(column) for column in columns]
        self.auto_add_non_listed_columns = auto_add_non_listed_columns

    def as_component_def(self, serializer: "Serializer"):
        return dict(
            columns=[column.as_component_def(serializer) for column in self.columns],
            auto_add_non_listed_columns=self.auto_add_non_listed_columns,
        )


class ResponsiveTableLayouts:
    def __init__(
        self,
        auto_generate_single_row_layout: bool = True,
        layouts: Optional[List[ResponsiveTableLayout]] = None,
        auto_generate_single_column_layout: bool = True,
    ):
        self.auto_generate_single_row_layout = auto_generate_single_row_layout
        self.layouts = layouts or []  # type: List[ResponsiveTableLayout]
        assert all((isinstance(layout, ResponsiveTableLayout) for layout in self.layouts))
        self.auto_generate_single_column_layout = auto_generate_single_column_layout

    def as_component_def(self, serializer: "Serializer"):
        return dict(
            auto_generate_single_row_layout=self.auto_generate_single_row_layout,
            layouts=[layout.as_component_def(serializer) for layout in self.layouts],
            auto_generate_single_column_layout=self.auto_generate_single_column_layout,
        )
