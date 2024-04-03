import { APIConsumer } from '../api_consumer/namespace';

export namespace DfForm {
  export interface ChoicesJSON {
    id: any;
    text: any;
  }

  export interface AJAXJSON {
    url_reverse: string;
    placeholder: string;
    additional_parameters: string;
    query_field: string;
    value_field: string;
    text_field: string;
  }

  export type StatementJSON = [ string | StatementJSON, number, any | StatementJSON ] | null;

  export interface FormFieldJSON {
    uuid: string;
    name: string;
    label: string;
    placeholder: string;
    alignment: 'left' | 'right' | 'center' | 'decimal';
    visibility: { form: number, table: number };
    render_params: DfForm.RenderParamsJSON;
    read_only: true | any; // boolean
    choices: ChoicesJSON[];
    ajax: AJAXJSON;
    width_classes: string; // bootstrap column width classes TODO: should be changed to something platform agnostic
    help_text: string;
    allow_null: boolean;
    conditional_visibility: DfForm.StatementJSON;
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
    form_format?: string;
    multiple?: boolean;
    allow_tags?: boolean;
    table?: string;
    table_show_zeroes?: boolean;
  }

  export type FormLayoutFieldsCollection = { [key: string]: DfForm.FormFieldJSON };

  export interface FormLayoutRowsColumnJSON {
    type: 'column' | 'group';
    field: string;
    title?: string;
    layout?: DfForm.FormLayoutJSON;
  }

  export interface FormLayoutRowJSON {
    component: string;
    columns: FormLayoutRowsColumnJSON[];
  }

  export interface FormLayoutJSON {
    field_name: string;
    component_name: string;
    fields: FormLayoutFieldsCollection;
    rows: FormLayoutRowJSON[];
    size: string;
  }
}

export default DfForm;
