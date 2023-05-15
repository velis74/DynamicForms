import { DfForm } from '../namespace';

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

  formComponentDef?: DfForm.FormComponentDefinition;

  constructor(params: DfForm.RenderParamsJSON) {
    this.inputType = params.input_type;
    this.fieldCSSClass = params.field_class || '';

    // Text input
    this.pattern = params.pattern || '';
    this.min = params.min || 0;
    this.max = params.max || 1E20;
    this.minLength = params.min_length || 0;
    this.maxLength = params.max_length || 1E20;

    // text input, translated into HTML attributes
    this.step = params.step || 1;
    this.size = params.size || 40;

    // DateTime
    this.formFormat = params.form_format || '';

    // select
    this.multiple = params.multiple || false;
    this.allowTags = params.allow_tags || false;

    // form definition
    this.formComponentDef = params.form_component_def;
  }
}
