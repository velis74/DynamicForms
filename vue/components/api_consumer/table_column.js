import ColumnDisplay from './table_column_display';

export class TableColumn {
  constructor(initialData) {
    // Below we circumvent having to declare an internal variable which property getters would be reading from
    Object.defineProperties(this, {
      name: { get() { return initialData.name; }, enumerable: true },
      label: { get() { return initialData.label; }, enumerable: true },
      ordering: { get() { return initialData.ordering; }, enumerable: true },
      // alignment: { get() { return initialData.alignment; }, enumerable: true },
      align: {
        get() {
          if (initialData.alignment === 'decimal') return 'right';
          return initialData.alignment;
        },
        enumerable: true,
      },
      visibility: {
        get() {
          const vis = initialData.visibility.table;
          if (!Object.values(ColumnDisplay).includes(vis)) {
            console.warn(
              `Table column came with visibility set to ${vis}, but we don't know that constant`,
            );
          }
          return vis;
        },
        enumerable: true,
      },
    });
  }
}

export function TableColumns(columnNames, fields) {
  return columnNames.map((columnName) => new TableColumn(fields[columnName]));
}
