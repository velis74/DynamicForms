import { DfForm } from '../form/namespace';

export namespace DfTable {
  export type CSSAlignment = 'left' | 'right' | 'center';
  export type InitialDataCSSAlignment = CSSAlignment | 'decimal';

  export interface VisibilityJSON {
    form: number; // ColumnDisplay
    table: number; // ColumnDisplay
  }

  export interface ColumnJSON {
    name: string;
    label: string;
    alignment: InitialDataCSSAlignment;
    ordering: string;
    render_params: DfForm.RenderParamsJSON;
    visibility: VisibilityJSON;
    table_classes?: string;
  }

  export interface ResponsiveLayoutInterface {

  }

  export interface RowControlDataInterface {
    row_css_class?: string;
    row_css_style?: string;
    actions?: any[];
  }

  export interface RowControlStructure {
    measuredHeight: number | null;
    isShowing: boolean;
    componentName: string;
    CSSClass: string;
    CSSStyle: string;
  }

  export interface RowDataInterface {
    [key: string]: any;

    df_control_data?: RowControlDataInterface;
  }

  export type RowsData = {
    results: RowDataInterface[];
    next: string;
  } | RowDataInterface[];

  export interface ResponsiveTableLayoutDefinition {
    columns: (string | string[])[];
    autoAddNonListedColumns: boolean;
  }

  export interface ResponsiveTableLayoutsDefinition {
    auto_generate_single_row_layout: boolean;
    auto_generate_single_column_layout: boolean;
    layouts: {
      columns: string[];
      auto_add_non_listed_columns: boolean;
    }[];
  }
}
