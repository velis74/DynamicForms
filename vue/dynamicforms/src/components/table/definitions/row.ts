import { reactive } from 'vue';

import { DfTable } from '../namespace';

/**
 * TableRow contains data for table row columns. Basically object with key(field.name) = value(field data)
 * TODO: TableRow is VERY similar to FormPayload object in service it provides. Maybe they should be the same class
 *  or at least derive from a common ancestor?
 */
export default class TableRow {
  [key: string]: any;

  dfControlStructure: DfTable.RowControlStructure;

  constructor(rowData: DfTable.RowDataInterface) {
    const dfControlData = rowData.df_control_data || {};
    delete rowData.df_control_data;
    Object.assign(this, rowData);

    this.dfControlStructure = reactive({
      measuredHeight: null, // will be filled out when it is rendered into DOM
      isShowing: true, // row is currently in ViewPort and should fully render
      componentName: 'GenericTRow', // default row renderer
      CSSClass: dfControlData.row_css_class || '',
      CSSStyle: dfControlData.row_css_style || '',
    });
    Object.defineProperty(
      this.dfControlStructure,
      'actions',
      { get() { return dfControlData.actions || ''; }, enumerable: true },
    );
  }

  setMeasuredHeight(value: number) {
    if (this.dfControlStructure.measuredHeight !== value) {
      this.dfControlStructure.measuredHeight = value;
    }
  }

  setIsShowing(value: boolean) {
    if (this.dfControlStructure.isShowing !== value) {
      this.dfControlStructure.isShowing = value;
    }
  }
}
