import { reactive } from 'vue';

import { APIConsumer } from '../../api_consumer/namespace';
import { DfTable } from '../namespace';

import TableRow from './row';

export default class TableRows {
  logic: APIConsumer.ConsumerLogicBaseInterface;

  visibilityHandler: (rowPk?: number) => boolean | { callback: (isVisible: boolean) => void, once?: boolean };

  next: string | null;

  data: TableRow[];

  rowIndices: { [key: string]: number };

  constructor(logic: APIConsumer.ConsumerLogicBaseInterface, rowsData: DfTable.RowsData) {
    this.logic = logic;
    // function to pass to vue-observe-visibility to know when to load more rows
    this.visibilityHandler = () => {
      console.log('Empty handler');
      return false;
    };

    this.next = null; // url to fetch rows after currently last row
    this.data = reactive([]); // actual rows
    this.rowIndices = {}; // stores primaryKey -> {index} in data for faster lookup when deleting & updating

    if (rowsData && 'results' in rowsData && Array.isArray(rowsData.results)) {
      // REST response was paginated. actual rows in results, next and prev pointer provided as well
      this.updateRows(rowsData.results);
      this.next = rowsData.next;
      this.decorate(this.data);
    } else if (Array.isArray(rowsData)) {
      // REST response was an unpaginated array of rows. We don't decorate it because all rows had already been fetched
      this.updateRows(rowsData);
    }
  }

  /**
   * Creates a visibilityHandler on first and last row so that we can trigger loading new rows when they come in view
   */
  decorate(newRows: DfTable.RowDataInterface[]) {
    if (!newRows || !newRows.length) {
      // No new rows received, so let's not monitor visibility for further loading
      this.visibilityHandler = () => {
        console.log('Empty handler 2');
        return false;
      };
      return;
    }
    const pkName = this.logic.pkName;
    const triggerRow1 = newRows[0][pkName];
    const triggerRow2 = newRows[newRows.length - 1][pkName];
    const self = this;

    this.visibilityHandler = (rowPk?: number) => {
      if (triggerRow1 !== rowPk && triggerRow2 !== rowPk) return false;
      return { callback: (isVisible) => { self.loadMoreRows(isVisible); }, once: true };
    };
  }

  async loadMoreRows(isVisible: boolean) {
    if (!isVisible || !this.next) return;
    const newRows = await (<APIConsumer.ConsumerLogicAPIInterface> this.logic).fetchNewRows(this.next);
    if (newRows !== undefined) {
      this.updateRows(newRows.results);
      this.next = newRows.next; // replace next so we can load another set of rows
      this.decorate(newRows.results);
    }
  }

  updateRows(newRows: DfTable.RowDataInterface[]) {
    // let wasModified = false;
    const pkName = this.logic.pkName;
    newRows.map((row) => {
      const rowData = new TableRow(row);
      const pk = rowData[pkName];
      const pkIdx = this.rowIndices[pk];
      if (pkIdx != null) {
        this.data[pkIdx] = rowData;
        // wasModified = true;
      } else {
        // TODO: Currently all added records shows on current last table row. It should be dependent on ordering, etc.
        const newLength = this.data.push(rowData);
        this.rowIndices[pk] = newLength - 1;
      }
      return null;
    });
    // if (wasModified) this.drawSeq++;
  }

  reIndex() {
    this.rowIndices = {};
    const pkName: string = this.logic.pkName;
    this.data.forEach((row: TableRow, index: number) => { this.rowIndices[row[pkName]] = index; });
  }

  deleteRow(tableRowId: string) {
    this.data.splice(this.rowIndices[tableRowId], 1);
    this.reIndex();
  }
}
