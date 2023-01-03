import _ from 'lodash';

import DisplayMode from '@/components/classes/display-mode';
import IndexedArray from '@/components/classes/indexed-array';
import FormField from '@/components/form/definitions/field';
import FormPayload from '@/components/form/definitions/form-payload';

import TableColumns from '@/components/table/definitions/columns';
import TableRow from '@/components/table/definitions/row';

export default class TableFilterRow {
  private readonly columns: IndexedArray | any = null;
  private value: TableRow | null = null;
  private readonly payload: FormPayload | undefined;

  constructor(filterData: any) {
    if (!filterData) {
      this.columns = [];
      return;
    }
    const filterDataNoActions = _.filter(filterData.columns, (cl) => !_.includes(cl.name, '#actions'));
    let record = _.clone(filterData.record);
    record = _.mapValues(record, () => null);
    this.value = new TableRow(record);
    const fields: any = {};
    filterDataNoActions.forEach((column) => {
      fields[column.name] = column;
    });
    // eslint-disable-next-line max-len
    const filteredCols = _.filter(TableColumns(filterDataNoActions.map((col) => col.name), fields), (c) => c.visibility === DisplayMode.FULL);
    filteredCols.forEach((v) => {
      const fieldPayload = fields[v.name];
      fieldPayload.help_text = null;
      fieldPayload.label = null;
      v.formFieldInstance = new FormField(fieldPayload);
    });
    this.columns = new IndexedArray(filteredCols);
    this.payload = new FormPayload(record, { fields: this.columns });
  }
}
