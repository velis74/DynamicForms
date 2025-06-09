import { DfForm } from '../namespace';

export default class RenderParams {
  inputType: string;

  fieldCSSClass?: string;

  pattern?: string;

  min?: number;

  max?: number;

  minLength: number;

  maxLength: number;

  step?: number;

  size?: number;

  formDateFormat?: string;

  formTimeFormat?: string;

  multiple?: boolean;

  allowTags?: boolean;

  formComponentDef?: DfForm.FormComponentDefinition;

  constructor(params: DfForm.RenderParamsJSON) {
    this.inputType = params.input_type;
    this.fieldCSSClass = params.field_class;

    // Text input
    this.pattern = params.pattern;
    this.min = params.min;
    this.max = params.max;
    this.minLength = params.min_length ?? 0;
    this.maxLength = params.max_length ?? 1E20;

    // text input, translated into HTML attributes
    this.step = params.step;
    this.size = params.size;

    // DateTime
    this.formDateFormat = params.form_date_format;
    this.formTimeFormat = params.form_time_format;

    // select
    this.multiple = params.multiple;
    this.allowTags = params.allow_tags;

    // form definition
    this.formComponentDef = params.form_component_def;
  }
}
