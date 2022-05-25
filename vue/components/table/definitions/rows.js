import _ from 'lodash';

import TableRow from './row';

export default class TableRows {
  constructor(logic, rowsData) {
    this.logic = logic;
    this.visibilityHandler = () => false; // function to pass to vue-observe-visibility to know when to load more rows

    this.next = null; // url to fetch rows after currently last row
    this.data = []; // actual rows
    this.rowIndices = {}; // stores primaryKey -> {index} in data for faster lookup when deleting & updating

    if (rowsData && rowsData.results && Array.isArray(rowsData.results)) {
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
  decorate(newRows) {
    if (!newRows || !newRows.length) {
      // No new rows received, so let's not monitor visibility for further loading
      this.visibilityHandler = () => false;
      return;
    }
    const pkName = this.logic.pkName;
    const triggerRow1 = newRows[0][pkName];
    const triggerRow2 = newRows[newRows.length - 1][pkName];
    const self = this;

    this.visibilityHandler = (rowPk) => {
      if (triggerRow1 !== rowPk && triggerRow2 !== rowPk) return false;
      return { callback: (isVisible) => { self.loadMoreRows(isVisible); }, once: true };
    };
  }

  async loadMoreRows(isVisible) {
    if (!isVisible || !this.next) return;
    const newRows = await this.logic.fetch(this.next, true);
    this.updateRows(newRows.results);
    this.next = newRows.next; // replace next so we can load another set of rows
    this.decorate(newRows.results);
  }

  updateRows(newRows) {
    let wasModified = false;
    const pkName = this.logic.pkName;
    newRows.map((row) => {
      const rowData = row instanceof TableRow ? row : new TableRow(row);
      const pk = rowData[pkName];
      const pkIdx = this.rowIndices[pk];
      if (pkIdx != null) {
        this.data[pkIdx] = rowData;
        wasModified = true;
      } else {
        // TODO: Currently all added records shows on current last table row. It should be dependent on ordering, etc.
        const newLength = this.data.push(rowData);
        this.rowIndices[pk] = newLength - 1;
      }
      return null;
    });
    if (wasModified) this.drawSeq++;
  }

  reIndex() {
    this.rowIndices = _.invert(_.mapValues(this.data, (row) => row[this.logic.pkName]));
  }

  deleteRow(tableRowId) {
    this.data.splice(this.rowIndices[tableRowId], 1);
    this.reIndex();
  }
}
