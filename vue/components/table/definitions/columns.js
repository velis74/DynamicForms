import TableColumn from './column';

export default function TableColumns(columnNames, fields) {
  return columnNames.map((columnName) => new TableColumn(fields[columnName]));
}
