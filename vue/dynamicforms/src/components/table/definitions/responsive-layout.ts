// TODO: rowspan (field spanning multiple rows)
// TODO: speed - currently there's way too much DOM

// eslint-disable-next-line max-classes-per-file
import _ from 'lodash';
import { reactive } from 'vue';

import DisplayMode from '../../classes/display-mode';
import IndexedArray from '../../classes/indexed-array';
import { DfForm } from '../../form/namespace';
import { DfTable } from '../namespace';

import TableColumn from './column';

export class ColumnGroupRow {
  fields: TableColumn[];

  constructor(fieldsDef: string | string[], renderedColumns: IndexedArray<TableColumn>) {
    const fields = Array.isArray(fieldsDef) ? fieldsDef : [fieldsDef];
    this.fields = fields.map((field: string) => {
      const column = renderedColumns[field] ?? renderedColumns[`${field}-display`];
      if (column === undefined) {
        console.error(`Column ${field} does not exist`, renderedColumns);
        return null;
      }
      return column;
    });
  }
}

export class ColumnGroup extends TableColumn {
  rows: ColumnGroupRow[];

  fields!: TableColumn[];

  constructor(layout: ResponsiveLayout, columnDef: string[], renderedColumns: IndexedArray<TableColumn>) {
    super({
      name: `ColumnGroup${layout.columns.length}`,
      label: '',
      alignment: 'left',
      ordering: '',
      visibility: { table: DisplayMode.FULL, form: DisplayMode.SUPPRESS },
      render_params: <DfForm.RenderParamsJSON><unknown>{ table: '#ColumnGroup' },
      table_classes: '',
    }, []);

    this.setLayout(layout);
    this.rows = columnDef.map((row) => new ColumnGroupRow(row, renderedColumns));

    Object.defineProperties(this, {
      fields: {
        get() {
          return this.rows.reduce((result: TableColumn[], row: ColumnGroupRow) => {
            row.fields.forEach((field: TableColumn) => result.push(field));
            return result;
          }, []);
        },
        enumerable: true,
      },
    });
  }
}

export class ResponsiveLayout implements DfTable.ResponsiveLayoutInterface {
  totalWidth!: number;

  columns: IndexedArray<TableColumn>;

  rows: number;

  constructor(definition: DfTable.ResponsiveTableLayoutDefinition, renderedColumns: IndexedArray<TableColumn>) {
    const columnsDef = Array.isArray(definition) ? definition : (definition.columns || []);
    this.columns = new IndexedArray<TableColumn>([]);
    columnsDef.forEach((column: string[]) => {
      this.columns.push(
        column.length === 1 ?
          renderedColumns[column[0]] ?? renderedColumns[`${column[0]}-display`] :
          new ColumnGroup(this, column, renderedColumns),
      );
    });
    this.rows = Math.max(1, ...this.columns.map(
      (col: TableColumn | ColumnGroup) => (col instanceof ColumnGroup ? col.rows.length : 1),
    ));
    this.totalWidth = 0;

    // add non-listed columns
    if (definition.autoAddNonListedColumns) {
      const usedColumns = new Set<string>();
      const allColumns = new Set(renderedColumns.map((col) => col.name));
      this.columns.forEach((columnGroup: TableColumn | ColumnGroup) => {
        if (columnGroup instanceof ColumnGroup) {
          columnGroup.rows.forEach((row: ColumnGroupRow) => {
            row.fields.forEach((column: TableColumn) => usedColumns.add(column.name));
          });
        } else {
          usedColumns.add(columnGroup.name);
        }
      });
      const missingColumns = new Set([...allColumns].filter((item) => !usedColumns.has(item)));
      renderedColumns.forEach((column) => {
        if (missingColumns.has(column.name)) { this.columns.push(renderedColumns[column.name]); }
      });
    }
  }
}

export class ResponsiveLayouts {
  layouts: ResponsiveLayout[];

  constructor(
    renderedColumns: IndexedArray<TableColumn>,
    responsiveTableLayoutsDef: DfTable.ResponsiveTableLayoutsDefinition | null,
  ) {
    this.layouts = [];

    // one row, columns next to each other variant is generated automatically
    // Any columns not listed in the array will be auto-added to first row at the end (here, none are listed)
    if (responsiveTableLayoutsDef == null || responsiveTableLayoutsDef.auto_generate_single_row_layout) {
      this.pushLayout(new ResponsiveLayout({ autoAddNonListedColumns: true, columns: [] }, renderedColumns));
      renderedColumns.forEach((column) => column.setLayout(this.layouts[0]));
    }

    if (responsiveTableLayoutsDef && responsiveTableLayoutsDef.layouts) {
      // Intermediate layouts, each should be narrower than the previous (otherwise it will never be drawn)
      responsiveTableLayoutsDef.layouts.forEach((layoutDef) => {
        this.pushLayout(new ResponsiveLayout({
          columns: layoutDef.columns,
          autoAddNonListedColumns: layoutDef.auto_add_non_listed_columns,
        }, renderedColumns));
      });
    }

    // n rows, 1 column variant is generated automatically
    if (responsiveTableLayoutsDef == null || responsiveTableLayoutsDef.auto_generate_single_column_layout) {
      this.pushLayout(
        new ResponsiveLayout(
          { columns: [renderedColumns.map((column) => column.name)], autoAddNonListedColumns: true },
          renderedColumns,
        ),
      );
    }
  }

  pushLayout(layout: ResponsiveLayout) {
    // For some reason, Vue will not decorate totalWidth property when used from table.js.
    // Making the layout observable will
    this.layouts.push(reactive(layout) as ResponsiveLayout);
  }

  recalculate(containerWidth: number): ResponsiveLayout {
    return this.layouts.find((layout: ResponsiveLayout) => {
      layout.totalWidth = _.sum(layout.columns.map((el) => el.maxWidth ?? 0));
      return layout.totalWidth <= containerWidth;
    }) ?? this.layouts[this.layouts.length - 1];
  }
}
