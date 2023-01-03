import type { UnwrapNestedRefs } from 'vue';
import { reactive } from 'vue';

interface IControlData {
  row_css_class?: string;
  row_css_style?: string;
  actions?: string;
}

export default class TableRow {
  public dfControlStructure: UnwrapNestedRefs<{ isShowing: boolean; measuredHeight: null; componentName: string }>;
  private dfControlData: IControlData;

  constructor(rowData: any) {
    this.dfControlData = rowData.df_control_data || {};
    delete rowData.df_control_data;
    Object.assign(this, rowData);

    this.dfControlStructure = reactive({
      measuredHeight: null, // will be filled out when it is rendered into DOM
      isShowing: true, // row is currently in ViewPort and should fully render
      componentName: 'GenericTRow', // default row renderer
    });
  }

  get CSSClass(): string { return this.dfControlData.row_css_class || ''; }
  get CSSStyle(): string { return this.dfControlData.row_css_style || ''; }
  get actions(): string { return this.dfControlData.actions || ''; }

  setMeasuredHeight(value: any) {
    if (this.dfControlStructure.measuredHeight !== value) {
      this.dfControlStructure.measuredHeight = value;
    }
  }

  setIsShowing(value: any) {
    if (this.dfControlStructure.isShowing !== value) {
      this.dfControlStructure.isShowing = value;
    }
  }
}
