import { reactive } from 'vue';

import RowControlStructure = DfTable.RowControlStructure;
import RowDataInterface = DfTable.RowDataInterface;

export default class TableRow { // eslint-disable-line max-classes-per-file
  [key: string]: any;

  dfControlStructure: RowControlStructure;

  constructor(rowData: RowDataInterface) {
    const dfControlData = rowData.df_control_data || {};
    delete rowData.df_control_data;
    Object.assign(this, rowData);

    this.dfControlStructure = reactive({
      measuredHeight: null, // will be filled out when it is rendered into DOM
      isShowing: true, // row is currently in ViewPort and should fully render
      componentName: 'GenericTRow', // default row renderer
    });
    Object.defineProperties(this.dfControlStructure, {
      CSSClass: { get() { return dfControlData.row_css_class || ''; }, enumerable: true },
      CSSStyle: { get() { return dfControlData.row_css_style || ''; }, enumerable: true },
      actions: { get() { return dfControlData.actions || ''; }, enumerable: true },
    });
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