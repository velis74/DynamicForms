import TableColumn from '@/components/table/definitions/column';

export default function TableColumns(columnNames: Array<string>, fields: any) {
  const orderingArray: Array<any> = [];
  const res = columnNames.map((columnName: string) => new TableColumn(fields[columnName], orderingArray))
  // We will also clear any non-assigned sorting segments from the orderingArray
  for (let i = orderingArray.length - 1; i >= 0; i--) {
    if (!orderingArray[i]) orderingArray.splice(i, 1);
  }
  return res;
}
