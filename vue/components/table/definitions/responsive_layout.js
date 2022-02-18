// eslint-disable-next-line max-classes-per-file
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
  constructor(columnDef, renderedColumns, cgIndex) {
    super({
      name: `ColumnGroup${cgIndex}`,
      label: '',
      alignment: 'left',
      ordering: '',
      visibility: { table: DisplayMode.FULL },
      render_params: { table: '#ColumnGroup' },
    }, []);
    const rows = Array.isArray(columnDef) ? columnDef : (columnDef.columns || []);
    this.rows = rows.map((row) => new ColumnGroupRow(row, renderedColumns));

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
    const def = this.sanitizeColumnsDefinition(definition, renderedColumns);
    this.rows = def.rows;

    Object.defineProperties(this, {
      totalWidth: { get() { return this.getTotalWidth(); }, enumerable: true },
      columns: { get() { return def.columns; }, enumerable: true },
    });

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
      let index = this.columns.length;
      renderedColumns.forEach((column) => {
        if (missingColumns.has(column.name)) {
          this.columns.push(new ColumnGroup([column.name], renderedColumns, index++));
        }
      });
    }
  }

  // eslint-disable-next-line class-methods-use-this
  sanitizeColumnsDefinition(definition, renderedColumns) {
    let columns = Array.isArray(definition) ? definition : (definition.columns || []);
    columns = new IndexedColumns(
      columns.map((column, index) => new ColumnGroup(column, renderedColumns, index)),
    );
    return { columns, rows: Math.max(1, ...columns.map((col) => col.rows.length)) };
  }

  getTotalWidth() {
    return this.columns.reduce((result, column) => result + column.maxWidth, 0);
  }
}

export class ResponsiveLayouts {
  constructor(renderedColumns/* TODO , responsiveColumns */) {
    this.layouts = [];

    // one row, columns next to each other variant is generated automatically
    // Any columns not listed in the array will be auto-added to first row at the end (here, none are listed)
    this.layouts.push(new ResponsiveLayout({ autoAddNonListedColumns: true }, renderedColumns));

    // two row layout
    // note how each "column" array has at most two members resulting in a two-row layout.
    // If there is only one member, that means an empty second row.
    // If any member is an array, that means group of fields
    this.layouts.push(new ResponsiveLayout({
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
    this.layouts.push(new ResponsiveLayout({
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
    this.layouts.push(
      new ResponsiveLayout({ columns: [renderedColumns.map((column) => column.name)] }, renderedColumns),
    );
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
