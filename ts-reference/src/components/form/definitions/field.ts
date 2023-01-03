import DisplayMode from '@/components/classes/display-mode';

// Checks if we are in development mode
const IS_DEVELOPMENT = (
  window.webpackHotUpdate || process.env.NODE_ENV === 'development'
);

interface VisibilityDefinition {
  form: string;
}

interface FieldRenderParams {
  input_type: any;
  field_class: any;
  pattern: any;
  min: any;
  max: any;
  min_length: any;
  max_length: any;
  step: any;
  size: any;
  form_format: any;
  multiple: boolean;
  allow_tags: boolean;
  form_component_name: any;
}

interface FieldDefinition {
  name: string;
  label: string;
  alignment: string;
  visibility: VisibilityDefinition;
  render_params: FieldRenderParams;
  read_only: boolean;
  choices: any;
  width_classes: any;
  help_text: string;
  allow_null: boolean;
  placeholder?: string;
}

function wrapInProxy(renderParams: any) {
  return new Proxy(renderParams, {
    get(target, prop) {
      if (Object.prototype.hasOwnProperty.call(target, prop)) {
        return Reflect.get(...arguments);
      }
      if (!(['toJSON', 'constructor', 'render', 'state', '_isVue'].includes(prop) || typeof prop === 'symbol')) {
        // these are called by Vue internals when inspecting in Vue devtools
        // console.error(`RenderParams doesn't have property named ${prop.toString()}`);
      }
      return target[prop];
    },
  });
}

class RenderParams {
  inputType: any;
  fieldCSSClass: any;
  maxLength: any;
  pattern: any;
  min: any;
  max: any;
  minLength: any;
  step: any;
  size: any;
  formFormat: any;
  multiple: any;
  allowTags: any;

  constructor(params: FieldRenderParams) {
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

  static create(params: any): RenderParams {
    return IS_DEVELOPMENT ? wrapInProxy(new RenderParams(params)) : new RenderParams(params);
  }
}

export default class FormField{
  private _renderKey: number = 0;
  private fieldDef: FieldDefinition;

  constructor(fieldDef: FieldDefinition) {
    this.fieldDef = fieldDef;
  }

  // Below we circumvent having to declare an internal variable which property getters would be reading from
  get name(): string { return this.fieldDef.name; }
  get label(): string { return this.fieldDef.label; }
  get align(): string { return this.fieldDef.alignment === 'decimal' ? 'right' : this.fieldDef.alignment; }
  get visibility(): any { return DisplayMode.get(this.fieldDef.visibility.form); }
  get renderParams(): RenderParams { return RenderParams.create(this.fieldDef.render_params); }
  get readOnly(): boolean { return this.fieldDef.read_only; }
  get componentName(): string { return this.fieldDef.render_params.form_component_name; }
  get choices(): any { return this.fieldDef.choices; }
  get widthClasses(): any { return this.fieldDef.width_classes; }
  get helpText(): string { return this.fieldDef.help_text; }
  get allowNull(): boolean { return this.fieldDef.allow_null; }
  get placeholder(): string | undefined { return this.fieldDef.placeholder; }

  get isVisible() { return (this.visibility !== DisplayMode.SUPPRESS && this.visibility !== DisplayMode.HIDDEN); }

  setVisibility(visibility: any) {
    let displayMode;
    if (DisplayMode[visibility]) {
      displayMode = DisplayMode[visibility];
    } else if (visibility) {
      displayMode = DisplayMode.FULL;
    } else {
      displayMode = DisplayMode.HIDDEN;
    }
    if (displayMode !== this.fieldDef.visibility.form) {
      this.fieldDef.visibility.form = displayMode;
      this._renderKey++; // notify the components to redraw
    }
  }
}
