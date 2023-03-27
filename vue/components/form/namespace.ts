namespace DfForm {
  export interface ChoicesJSON {
    id: any;
    text: any;
  }

  export interface AJAXJSON {
    url_reverse: string;
    placeholder: string;
    additional_parameters: string;
    query_field: string;
  }

  export interface FormFieldJSON {
    name: string;
    label: string;
    alignment: 'left' | 'right' | 'center' | 'decimal';
    visibility: { form: number, table: number };
    render_params: DfForm.RenderParamsJSON;
    read_only: true | any; // boolean
    choices: ChoicesJSON[];
    ajax: AJAXJSON;
    width_classes: string; // bootstrap column width classes TODO: should be changed to something platform agnostic
    help_text: string;
    allow_null: boolean;
  }

  export interface RenderParamsJSON {
    input_type: string;
    form_component_def: Object;
    form_component_name: string;
    field_class: string;
    pattern: string;
    min: number;
    max: number;
    min_length: number;
    max_length: number;
    step: number;
    size: number;
    form_format: string;
    multiple: boolean;
    allow_tags: boolean;
    table: string;
  }
}
