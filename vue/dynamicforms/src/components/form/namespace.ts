import { APIConsumer } from '../api_consumer/namespace';

export namespace DfForm {
  export interface ChoicesJSON {
    id: any;
    text: any;
    icon: any;
  }

  export interface AJAXJSON {
    url_reverse: string;
    placeholder: string;
    additional_parameters: string;
    query_field: string;
    value_field: string;
    text_field: string;
    icon_field: string;
  }

  export type StatementJSON = [string | StatementJSON, number, any | StatementJSON] | null;

  export interface FormFieldJSON {
    uuid: string;
    name: string | null;
    label: string;
    placeholder: string;
    alignment: 'left' | 'right' | 'center' | 'decimal';
    visibility: { form: number, table: number };
    render_params: DfForm.RenderParamsJSON;
    read_only: true | any; // boolean
    choices: ChoicesJSON[];
    ajax?: AJAXJSON;
    colspan: number;
    help_text: string;
    allow_null: boolean;
    conditional_visibility?: DfForm.StatementJSON;
  }

  export interface FormFieldsJSON {
    [key: string]: FormFieldJSON;
  }

  export interface FormComponentDefinition extends APIConsumer.TableUXDefinition {
    detail_url: string;
  }

  export interface RenderParamsJSON {
    input_type: string;
    form_component_name: string;
    form_component_def?: DfForm.FormComponentDefinition;
    field_class?: string;
    pattern?: string;
    min?: number;
    max?: number;
    min_length?: number;
    max_length?: number;
    step?: number;
    size?: number;
    form_date_format?: string;
    form_time_format?: string;
    multiple?: boolean;
    allow_tags?: boolean;
    table?: string;
    table_show_zeroes?: boolean;
  }

  export type FormLayoutFieldsCollection = { [key: string]: DfForm.FormFieldJSON };
}

export namespace FormLayoutNS {
  /*
  interfaces for dynamicforms.layout definitions
   */
  export interface LayoutInterface {
    rows: RowInterface[];
    fields: DfForm.FormLayoutFieldsCollection;
    size?: string;
    header_classes?: string;
    component_name: string;
  }

  export interface RowInterface {
    component_name: string;
    columns: (ColumnInterface | GroupInterface)[];
  }

  export interface ColumnInterface {
    type: 'column' | 'group';
    field: string;
    component_name: string;
    colspan?: number;
  }

  export interface GroupInterface extends ColumnInterface {
    footer?: string;
    title?: string;
    uuid: string;
    layout: LayoutInterface;
  }

  export type ColumnOrGroupInterface = GroupInterface | ColumnInterface;
}

export namespace FormLayoutTypeGuards {
  export function isGroupTemplate(col: FormLayoutNS.ColumnOrGroupInterface): col is FormLayoutNS.GroupInterface {
    return col.type === 'group';
  }

  export function isLayoutTemplate(layout: any): layout is FormLayoutNS.LayoutInterface {
    return 'rows' in layout;
  }
}
