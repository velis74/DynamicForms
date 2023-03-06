namespace DfTable {
  export interface RowControlDataInterface {
    row_css_class?: string;
    row_css_style?: string;
    actions?: any[];
  }

  export interface RowControlStructure {
    measuredHeight: number | null;
    isShowing: boolean;
    componentName: string;
  }

  export interface RowDataInterface {
    [key: string]: any;

    df_control_data?: RowControlDataInterface;
  }

  export type RowsData = {
    results: RowDataInterface[];
    next: string;
  } | RowDataInterface[];
}
