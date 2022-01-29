export class TableColumn {
  constructor(initialData) {
    // Below we circumvent having to declare an internal variable which property getters would be reading from
    Object.defineProperties(this, {
      name: { get() { return initialData.name; } },
      ordering: { get() { return initialData.ordering; } },
      alignment: { get() { return initialData.alignment; } },
    });
  }
}

export function TableColumns(columnNames, fields) {
  return columnNames.map((columnName) => new TableColumn(fields[columnName]));
}
