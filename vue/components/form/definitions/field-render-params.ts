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
}

export default class RenderParams {
  inputType: string;

  fieldCSSClass: string;

  pattern: string;

  min: number;

  max: number;

  minLength: number;

  maxLength: number;

  step: number;

  size: number;

  formFormat: string;

  multiple: boolean;

  allowTags: boolean;

  constructor(params: RenderParamsJSON) {
    this.inputType = params.input_type;
    this.fieldCSSClass = params.field_class;

    // Text input
    this.pattern = params.pattern;
    this.min = params.min;
    this.max = params.max;
    this.minLength = params.min_length || 0;
    this.maxLength = params.max_length || 1E20;

    // text input, translated into HTML attributes
    this.step = params.step;
    this.size = params.size;

    // DateTime
    this.formFormat = params.form_format;

    // select
    this.multiple = params.multiple;
    this.allowTags = params.allow_tags;
  }
}
