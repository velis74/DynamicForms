import ColumnDisplay from '../util/display_mode';

export class TableColumn {
  constructor(initialData) {
    // Below we circumvent having to declare an internal variable which property getters would be reading from
    Object.defineProperties(this, {
      name: { get() { return initialData.name; }, enumerable: true },
      label: { get() { return initialData.label; }, enumerable: true },
      ordering: { get() { return initialData.ordering; }, enumerable: true },
      align: {
        get() {
          if (initialData.alignment === 'decimal') return 'right';
          return initialData.alignment;
        },
        enumerable: true,
      },
      visibility: { get() { return ColumnDisplay.get(initialData.visibility.table); }, enumerable: true },
    });
  }
}

export function TableColumns(columnNames, fields) {
  return columnNames.map((columnName) => new TableColumn(fields[columnName]));
}
