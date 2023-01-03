// TODO: rowspan (field spanning multiple rows)
// TODO: speed - currently there's way too much DOM

// eslint-disable-next-line max-classes-per-file
import _ from 'lodash';
import { reactive } from 'vue';

import DisplayMode from '../../classes/display-mode';
import IndexedArray from '../../classes/indexed-array';

import TableColumn from './column';

export class ColumnGroupRow {
  private fields: any;

  constructor(fieldsDef: any, renderedColumns: any) {
    const fields = Array.isArray(fieldsDef) ? fieldsDef : [fieldsDef];
    this.fields = fields.map((field) => {
      const column = renderedColumns[field];
      if (column === undefined) {
        console.error(`Column ${field} does not exist`, renderedColumns);
        return null;
      }
      return column;
    });
  }
}

export class ColumnGroup extends TableColumn {
  rows: any;

  constructor(layout: any, columnDef: any, renderedColumns: any) {
    super({
      name: `ColumnGroup${layout.columns.length}`,
      label: '',
      alignment: 'left',
      ordering: '',
      visibility: { table: DisplayMode.FULL },
      render_params: { table: '#ColumnGroup' },
    }, []);

    this.setLayout(layout);
    this.rows = columnDef.map((row: any) => new ColumnGroupRow(row, renderedColumns));
  }

  get fields() {
    return this.rows.reduce((result: any, row: any) => {
      row.fields.forEach((field: any) => result.push(field));
      return result;
    }, []);
  }
}

export class ResponsiveLayout {
  private columns: IndexedArray;
  private rows: number;
  private totalWidth: number;

  constructor(definition: any, renderedColumns: any) {
    const columnsDef = Array.isArray(definition) ? definition : (definition.columns || []);
    this.columns = new IndexedArray([]);
    columnsDef.forEach((column: any) => {
      this.columns.push(
        column.length === 1 ?
          renderedColumns[column[0]] :
          new ColumnGroup(this, column, renderedColumns),
      );
    });
    this.rows = Math.max(1, ...this.columns.map((col: any) => (col.rows ? col.rows.length : 1)));
    this.totalWidth = 0;

    // add non-listed columns
    if (definition.autoAddNonListedColumns) {
      const usedColumns = new Set();
      const allColumns = new Set(renderedColumns.map((col: any) => col.name));
      this.columns.forEach((columnGroup: any) => {
        if (columnGroup instanceof ColumnGroup) {
          columnGroup.rows.forEach((row: any) => {
            row.fields.forEach((column: any) => usedColumns.add(column.name));
          });
        } else {
          usedColumns.add(columnGroup.name);
        }
      });
      const missingColumns = new Set([...allColumns].filter((item) => !usedColumns.has(item)));
      renderedColumns.forEach((column: any) => {
        if (missingColumns.has(column.name)) { this.columns.push(renderedColumns[column.name]); }
      });
    }
  }
}

export class ResponsiveLayouts {
  layouts: any[];

  constructor(renderedColumns: any, responsiveTableLayoutsDef: any) {
    this.layouts = [];

    // one row, columns next to each other variant is generated automatically
    // Any columns not listed in the array will be auto-added to first row at the end (here, none are listed)
    if (responsiveTableLayoutsDef == null || responsiveTableLayoutsDef.auto_generate_single_row_layout) {
      this.pushLayout(new ResponsiveLayout({ autoAddNonListedColumns: true }, renderedColumns));
      renderedColumns.forEach((column: any) => column.setLayout(this.layouts[0]));
    }

    if (responsiveTableLayoutsDef == null) return; // nothing more to do here

    // Intermediate layouts, each should be narrower than the previous (otherwise it will never be drawn)
    responsiveTableLayoutsDef.layouts.forEach((layoutDef: any) => {
      this.pushLayout(new ResponsiveLayout({
        columns: layoutDef.columns,
        autoAddNonListedColumns: layoutDef.auto_add_non_listed_columns,
      }, renderedColumns));
    });

    // n rows, 1 column variant is generated automatically
    if (responsiveTableLayoutsDef.auto_generate_single_row_layout) {
      this.pushLayout(
        new ResponsiveLayout({ columns: [renderedColumns.map((column: any) => column.name)] }, renderedColumns),
      );
    }
  }

  pushLayout(layout: any) {
    // For some reason, Vue will not decorate totalWidth property when used from table.js.
    // Making the layout observable will
    console.log('layout', layout);
    this.layouts.push(reactive(layout));
  }

  recalculate(containerWidth: number) {
    console.log('recalculate', this.layouts.length);
    return this.layouts.find((layout) => {
      layout.totalWidth = _.sum(layout.columns.map((el: any) => el.maxWidth ?? 0));
      console.log(layout.totalWidth, containerWidth);
      return layout.totalWidth <= containerWidth;
    }) ?? this.layouts[-1];
  }
}
