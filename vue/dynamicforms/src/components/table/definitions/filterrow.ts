import _ from 'lodash';

import DisplayMode from '../../classes/display-mode';
import IndexedArray from '../../classes/indexed-array';
import FormField from '../../form/definitions/field';
import FormPayload from '../../form/definitions/form-payload';
import { DfForm } from '../../form/namespace';

import TableColumn from './column';
import TableColumns from './columns';
import TableRow from './row';

export default class TableFilterRow {
  columns: IndexedArray<TableColumn>;

  private value: unknown;

  public payload: FormPayload;

  constructor(filterData: any) {
    if (!filterData) {
      this.columns = new IndexedArray([]);
      this.payload = FormPayload.create();
      return;
    }
    const filterDataNoActions = _.filter(filterData.columns, (cl) => !_.includes(cl.name, '#actions'));
    let record = _.clone(filterData.record);
    record = _.mapValues(record, () => null);
    this.value = new TableRow(record);
    const fields: DfForm.FormFieldsJSON = {};
    filterDataNoActions.forEach((column) => {
      fields[column.name] = column;
    });
    const filteredCols = _.filter(
      new TableColumns(filterDataNoActions.map((col) => col.name), fields),
      (c) => c.visibility === DisplayMode.FULL,
    );
    filteredCols.forEach((v: TableColumn) => {
      // if this is a resolved -display field, use the actual field's definition for filter row
      const fieldNameForFilterRow = v.name.replace(/-display$/, '');
      const fieldPayload = fields[fieldNameForFilterRow];
      // we don't want labels or help text in the filter row
      // TODO: I don't think this is the way to approach this issue. We have provide/inject and a field could easily
      //  retrieve information about being placed within filter row. When this was true, label and help text are
      //  simply not rendered despite being populated.
      fieldPayload.help_text = '';
      fieldPayload.label = '';
      v.formFieldInstance = new FormField(fieldPayload);
    });
    this.columns = new IndexedArray(filteredCols);
    this.payload = FormPayload.create(record, { fields: this.columns, rows: [], field_name: '', component_name: '' });
  }
}
