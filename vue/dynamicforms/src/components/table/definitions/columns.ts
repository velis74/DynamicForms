import { reactive } from 'vue';

import TableColumn from './column';

export default class TableColumns extends Array<TableColumn> {
  constructor(columnNames: string[], fields: { [key: string]: any }) {
    super();

    if (!(columnNames && fields)) return; // If Array default constructors are called, we don't handle our logic

    const orderingArray = reactive([]);
    const res = columnNames.map((columnName: string) => new TableColumn(fields[columnName], orderingArray));

    // We will also clear any non-assigned sorting segments from the orderingArray
    for (let i = orderingArray.length - 1; i >= 0; i--) {
      if (!orderingArray[i]) orderingArray.splice(i, 1);
    }

    this.push(...res);
  }
}
