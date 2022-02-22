// eslint-disable-next-line max-classes-per-file
import Vue from 'vue';

import TableColumn from './column';
import DisplayMode from './display_mode';
import IndexedColumns from './indexed_columns';

export class ColumnGroupRow {
  constructor(fieldsDef, renderedColumns) {
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
  constructor(layout, columnDef, renderedColumns) {
    super({
      name: `ColumnGroup${layout.columns.length}`,
      label: '',
      alignment: 'left',
      ordering: '',
      visibility: { table: DisplayMode.FULL },
      render_params: { table: '#ColumnGroup' },
    }, []);

    this.setLayout(layout);
    this.rows = columnDef.map((row) => new ColumnGroupRow(row, renderedColumns));

    Object.defineProperties(this, {
      fields: {
        get() {
          return this.rows.reduce((result, row) => {
            row.fields.forEach((field) => result.push(field));
            return result;
          }, []);
        },
        enumerable: true,
      },
    });
  }
}

export class ResponsiveLayout {
  constructor(definition, renderedColumns) {
    const columnsDef = Array.isArray(definition) ? definition : (definition.columns || []);
    this.columns = new IndexedColumns([]);
    columnsDef.forEach((column) => {
      this.columns.push(
        column.length === 1 ?
          renderedColumns[column[0]] :
          new ColumnGroup(this, column, renderedColumns),
      );
    });
    this.rows = Math.max(1, ...this.columns.map((col) => (col.rows ? col.rows.length : 1)));
    this.totalWidth = 0;

    // add non-listed columns
    if (definition.autoAddNonListedColumns) {
      const usedColumns = new Set();
      const allColumns = new Set(renderedColumns.map((col) => col.name));
      this.columns.forEach((columnGroup) => {
        if (columnGroup instanceof ColumnGroup) {
          columnGroup.rows.forEach((row) => {
            row.fields.forEach((column) => usedColumns.add(column.name));
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
  constructor(renderedColumns, responsiveTableLayoutsDef) {
    this.layouts = [];

    // one row, columns next to each other variant is generated automatically
    // Any columns not listed in the array will be auto-added to first row at the end (here, none are listed)
    if (responsiveTableLayoutsDef == null || responsiveTableLayoutsDef.auto_generate_single_row_layout) {
      this.pushLayout(new ResponsiveLayout({ autoAddNonListedColumns: true }, renderedColumns));
      renderedColumns.forEach((column) => column.setLayout(this.layouts[0]));
    }

    if (responsiveTableLayoutsDef == null) return; // nothing more to do here

    // Intermediate layouts, each should be narrower than the previous (otherwise it will never be drawn)
    responsiveTableLayoutsDef.layouts.forEach((layoutDef) => {
      this.pushLayout(new ResponsiveLayout({
        columns: layoutDef.columns,
        autoAddNonListedColumns: layoutDef.auto_add_non_listed_columns,
      }, renderedColumns));
    });

    // n rows, 1 column variant is generated automatically
    if (responsiveTableLayoutsDef.auto_generate_single_row_layout) {
      this.pushLayout(
        new ResponsiveLayout({ columns: [renderedColumns.map((column) => column.name)] }, renderedColumns),
      );
    }
  }

  pushLayout(layout) {
    // For some reason, Vue will not decorate totalWidth property when used from table.js.
    // Making the layout observable will
    this.layouts.push(Vue.observable(layout));
  }

  recalculate(containerWidth) {
    for (let i = 0; i < this.layouts.length; i++) {
      //  we're assuming each consecutive layout is narrower than the previous one
      if (this.layouts[i].totalWidth <= containerWidth) {
        // console.log(`layout ${i}: ${this.layouts[i].totalWidth} <= ${containerWidth}`);
        return this.layouts[i];
      }
    }
    // return last layout (one column) even if it is too wide still
    // console.log(`layout ${this.layouts.length - 1}: none <= ${containerWidth}`);
    return this.layouts[this.layouts.length - 1];
  }
}
