import _ from 'lodash';

import DisplayMode from '../../classes/display-mode';
import IndexedArray from '../../classes/indexed-array';
import FormField from '../../form/definitions/field';

import TableColumns from './columns';
import TableRow from './row';

export default class TableFilterRow { // eslint-disable-line max-classes-per-file
  constructor(filterData) {
    if (!filterData) {
      this.columns = [];
      return;
    }
    const filterDataNoActions = _.filter(filterData.columns, (cl) => !_.includes(cl.name, '#actions'));
    let record = _.clone(filterData.record);
    record = _.mapValues(record, () => null);
    this.value = new TableRow(record);
    const fields = {};
    filterDataNoActions.forEach((column) => {
      fields[column.name] = column;
    });
    // eslint-disable-next-line max-len
    const filteredCols = _.filter(TableColumns(filterDataNoActions.map((col) => col.name), fields), (c) => c.visibility === DisplayMode.FULL);
    filteredCols.forEach((v) => {
      const fieldPayload = fields[v.name];
      fieldPayload.help_text = null;
      fieldPayload.label = null;
      const fField = new FormField(fieldPayload);
      v.formFieldInstance = fField;
    });
    this.columns = new IndexedArray(filteredCols);
  }
}
