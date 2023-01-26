import TableColumn from './column';

export default function TableColumns(columnNames, fields) {
  const orderingArray = [];
  const res = columnNames.map((columnName) => new TableColumn(fields[columnName], orderingArray));
  // We will also clear any non-assigned sorting segments from the orderingArray
  for (let i = orderingArray.length - 1; i >= 0; i--) {
    if (!orderingArray[i]) orderingArray.splice(i, 1);
  }
  return res;
}
