import _ from 'lodash';

import DisplayMode from '../../classes/display-mode';
import IndexedArray from '../../classes/indexed-array';
import FormField from '../../form/definitions/field';
import FormPayload from '../../form/definitions/form-payload';

import TableColumn from './column';
import TableColumns from './columns';
import TableRow from './row';

export default class TableFilterRow { // eslint-disable-line max-classes-per-file
  columns: unknown[];

  value: unknown;

  constructor(filterData: any) {
    if (!filterData) {
      this.columns = [];
      return;
    }
    const filterDataNoActions = _.filter(filterData.columns, (cl) => !_.includes(cl.name, '#actions'));
    let record = _.clone(filterData.record);
    record = _.mapValues(record, () => null);
    this.value = new TableRow(record);
    const fields: { [key: string]: { help_text: string | null, label: string | null } } = {};
    filterDataNoActions.forEach((column) => {
      fields[column.name] = column;
    });
    // eslint-disable-next-line max-len
    const filteredCols = _.filter(
      TableColumns(filterDataNoActions.map((col) => col.name), fields),
      (c) => c.visibility === DisplayMode.FULL,
    );
    filteredCols.forEach((v: TableColumn) => {
      const fieldPayload = fields[v.name];
      fieldPayload.help_text = null;
      fieldPayload.label = null;
      v.formFieldInstance = new FormField(fieldPayload);
    });
    this.columns = new IndexedArray(filteredCols);
    this.payload = new FormPayload(record, { fields: this.columns });
  }
}
