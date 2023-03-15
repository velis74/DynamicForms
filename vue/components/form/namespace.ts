namespace DfForm {
  export interface RenderParamsJSON {
    input_type: string;
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
