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
    if (!isVisible) return;
    const newRows = await this.logic.fetch(this.next, true);
    this.updateRows(newRows.results);
    this.next = newRows.next; // replace next so we can load another set of rows
    this.decorate(newRows.results);
  }

  /**
   * Decorates the row with some control structures that will help with rendering
   */
  createRowControlStructure(row) { // eslint-disable-line class-methods-use-this
    row.dfControlStructure = {
      measuredHeight: null, // will be filled out when it is rendered into DOM
      isShowing: true, // row is currently in ViewPort and should fully render
      componentName: 'GenericTRow', // default row renderer
    };
  }

  updateRows(newRows) {
    let wasModified = false;
    const pkName = this.logic.pkName;

    // ind[item.id] = idx;
    newRows.map((item) => {
      const pk = item[pkName];
      const pkIdx = this.rowIndices[pk];
      this.createRowControlStructure(item);
      if (pkIdx != null) {
        this.data[pkIdx] = item;
        wasModified = true;
      } else {
        // TODO: Currently all added records shows on current last table row. It should be dependent on ordering, etc.
        const newLength = this.data.push(item);
        this.rowIndices[pk] = newLength - 1;
      }
      return null;
    });
    if (wasModified) this.drawSeq++;
  }

  /*
  function updateRowFromForm(table, tableRows) {
    return (rowData) => {
      const rowId = rowData.id;
      if (rowId) {
        apiClient
          .get(table.detail_url.replace('--record_id--', rowId), { headers: { 'x-viewmode': 'TABLE_ROW' } })
          .then((response) => {
            // first we map existing row ids to respective array indexes
            tableRows.updateRows([response.data]);
          })
          .catch((err) => { console.error(err); })
          .finally(() => { table.loading = false; });
      }
    };
  }

  function deleteRow(res, tableRows) {
    return (rowId, idIndices) => {
      const indices = idIndices || getRowIndices(tableRows);
      tableRows.splice(indices[rowId], 1);
      res.drawSeq++;
    };
  }
  */
}
