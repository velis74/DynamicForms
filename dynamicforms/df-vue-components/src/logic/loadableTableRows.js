import apiClient from '../apiClient';

function decorate(res, rows) {
  let triggerRow1 = null;
  let triggerRow2 = null;
  if (rows && rows.length) {
    triggerRow1 = rows[0].id;
    triggerRow2 = rows[rows.length - 1].id;
  }
  res.getVisibilityHandler = (rowId) => (triggerRow1 === rowId || triggerRow2 === rowId ? {
    callback: res.loadMoreRows, once: true,
  } : false);
}

function getRowIndices(tableRows) {
  return tableRows.reduce((ind, item, idx) => { ind[item.id] = idx; return ind; }, {});
}

function updateRows(tableRows) {
  return (newRows, idIndices) => {
    const indices = idIndices || getRowIndices(tableRows);

    newRows.map((item) => {
      // then we iterate through results updating any existing entries and adding new ones
      const idIdx = indices[item.id];
      if (idIdx != null) {
        tableRows[idIdx] = item;
      } else {
        // TODO: Currently all added records shows on current last table row. It should be dependent on ordering, etc.
        tableRows.push(item);
      }
      return null;
    });
  };
}

function deleteRow(tableRows) {
  return (rowId, idIndices) => {
    const indices = idIndices || getRowIndices(tableRows);
    tableRows.splice(indices[rowId], 1);
  };
}

function loadMoreRows(table, res) {
  return (isVisible) => {
    if (!isVisible) return;
    table.loading = true;
    apiClient
      .get(table.rows.next, { headers: { 'x-viewmode': 'TABLE_ROW', 'x-pagination': 1 } })
      .then((response) => {
        // first we map existing row ids to respective array indexes
        const idIndices = getRowIndices(table.rows.results);
        res.updateRows(response.data.results, idIndices);
        table.rows.next = response.data.next; // replace next so we can load another set of rows
        // finally create a new loadableRows so that it will load new rows based on this result set
        decorate(res, response.data.results.length && response.data.next ? response.data.results : null);
      })
      .catch((err) => { console.error(err); })
      .finally(() => { table.loading = false; });
  };
}

const LoadableTableRows = function LoadableTableRows(table, rowsData) {
  let res = [];
  let next = null;
  if (rowsData && rowsData.results && rowsData.results.constructor === Array) {
    res = rowsData.results;
    next = rowsData.next;
  }
  decorate(res, res.length && next ? res : null);
  res.loadMoreRows = loadMoreRows(table, res);
  res.updateRows = updateRows(table.rows.results);
  res.deleteRow = deleteRow(table.rows.results);
  return res;
};

export default LoadableTableRows;
