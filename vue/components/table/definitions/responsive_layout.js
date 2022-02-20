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

    const rows = Array.isArray(columnDef) ? columnDef : (columnDef.columns || []);
    this.rows = rows.map((row) => new ColumnGroupRow(row, renderedColumns));

    Object.defineProperties(this, {
      layout: { get() { return layout; }, enumerable: false },
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

  setMaxWidth(value) {
    if (value > this.maxWidth) {
      this.layout.totalWidth += value - (this.maxWidth || 0);
      super.setMaxWidth(value);
    }
  }
}

export class ResponsiveLayout {
  constructor(definition, renderedColumns) {
    const columnsDef = Array.isArray(definition) ? definition : (definition.columns || []);
    this.columns = new IndexedColumns([]);
    columnsDef.forEach((column) => this.columns.push(new ColumnGroup(this, column, renderedColumns)));
    this.rows = Math.max(1, ...this.columns.map((col) => col.rows.length));
    this.totalWidth = 0;

    // add non-listed columns
    if (definition.autoAddNonListedColumns) {
      const usedColumns = new Set();
      const allColumns = new Set(renderedColumns.map((col) => col.name));
      this.columns.forEach((columnGroup) => {
        columnGroup.rows.forEach((row) => {
          row.fields.forEach((column) => usedColumns.add(column.name));
        });
      });
      const missingColumns = new Set([...allColumns].filter((item) => !usedColumns.has(item)));
      renderedColumns.forEach((column) => {
        if (missingColumns.has(column.name)) {
          this.columns.push(new ColumnGroup(this, [column.name], renderedColumns));
        }
      });
    }
  }
}

export class ResponsiveLayouts {
  constructor(renderedColumns/* TODO , responsiveColumns */) {
    this.layouts = [];

    // one row, columns next to each other variant is generated automatically
    // Any columns not listed in the array will be auto-added to first row at the end (here, none are listed)
    this.pushLayout(new ResponsiveLayout({ autoAddNonListedColumns: true }, renderedColumns));

    // two row layout
    // note how each "column" array has at most two members resulting in a two-row layout.
    // If there is only one member, that means an empty second row.
    // If any member is an array, that means group of fields
    this.pushLayout(new ResponsiveLayout({
      columns: [
        ['id'],
        ['boolean_field', 'nullboolean_field'],
        ['char_field', 'slug_field'],
        ['email_field', 'url_field'],
        ['uuid_field', ['ipaddress_field', 'integer_field', 'nullint_field']],
        ['float_field', 'decimal_field'],
        [['datetime_field', 'date_field'], ['time_field', 'duration_field']],
      ],
      autoAddNonListedColumns: true,
    }, renderedColumns));

    // three row layout
    this.pushLayout(new ResponsiveLayout({
      columns: [
        ['id'],
        [
          ['boolean_field', 'nullboolean_field'],
          ['ipaddress_field', 'integer_field', 'nullint_field'],
          ['float_field', 'decimal_field'],
        ],
        [['char_field', 'slug_field'], ['email_field', 'url_field'], 'uuid_field'],
        [['datetime_field', 'date_field'], ['time_field', 'duration_field']],
      ],
      autoAddNonListedColumns: true,
    }, renderedColumns));

    // n rows, 1 column variant is generated automatically
    this.pushLayout(new ResponsiveLayout({ columns: [renderedColumns.map((column) => column.name)] }, renderedColumns));
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
