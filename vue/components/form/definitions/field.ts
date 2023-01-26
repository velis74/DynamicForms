/**
 * FormField is a JavaScript class representation of JSON form field declaration
 *
 * Note: we're just assembling every possible configuration into a flat structure here
 * This introduces properties that might have nothing to do with a particular field type
 * Example: only a select field uses the "choices" property, but it's there for all fields.
 * Some inheritance might have fixed this, but would also introduce additional complexity
 *   as we tried to determine the correct field type from various field properties
 *
 * So, right now we aren't doing anything about that!
 */
import DisplayMode from '../../classes/display-mode';

// Checks if we are in development mode
const IS_DEVELOPMENT = (
  window.webpackHotUpdate || process.env.NODE_ENV === 'development' // TODO: this is for webpack, not Vite
);

function wrapInProxy(renderParams) {
  return new Proxy(renderParams, {
    get(target, prop) {
      if (Object.prototype.hasOwnProperty.call(target, prop)) {
        return Reflect.get(...arguments); // eslint-disable-line prefer-rest-params
      }
      if (!(['toJSON', 'constructor', 'render', 'state', '_isVue'].includes(prop) || typeof prop === 'symbol')) {
        // these are called by Vue internals when inspecting in Vue devtools
        // TODO: ce odkomentiras, se bo usulo mio logov
        // console.error(`RenderParams doesn't have property named ${prop.toString()}`);
      }
      return target[prop];
    },
  });
}

function RenderParams(params) {
  this.inputType = params.input_type;
  this.fieldCSSClass = params.field_class;
  this.maxLength = params.max_length;

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

  return IS_DEVELOPMENT ? wrapInProxy(this) : this;
}

export default class FormField {
  public name!: string;

  public visibility!: number;

  public readOnly!: boolean;

  constructor(fieldDef) {
    // Below we circumvent having to declare an internal variable which property getters would be reading from
    Object.defineProperties(this, {
      fieldDef: { get() { return fieldDef; }, enumerable: false },

      name: { get() { return fieldDef.name; }, enumerable: true },
      label: { get() { return fieldDef.label; }, enumerable: true },
      align: {
        get() {
          if (fieldDef.alignment === 'decimal') return 'right';
          return fieldDef.alignment;
        },
        enumerable: true,
      },
      visibility: { get() { return DisplayMode.get(fieldDef.visibility.form); }, enumerable: true },
      renderParams: { get() { return new RenderParams(fieldDef.render_params); }, enumerable: true },
      readOnly: { get() { return fieldDef.read_only === true; }, enumerable: true },
      componentName: { get() { return fieldDef.render_params.form_component_name; }, enumerable: true },
      choices: { get() { return fieldDef.choices; }, enumerable: true },
      widthClasses: { get() { return fieldDef.width_classes; }, enumerable: true },
      helpText: { get() { return fieldDef.help_text; }, enumerable: true },
      allowNull: { get() { return fieldDef.allow_null; }, enumerable: true },
    });
  }

  get isVisible() { return (this.visibility !== DisplayMode.SUPPRESS && this.visibility !== DisplayMode.HIDDEN); }

  setVisibility(visibility) {
    let displayMode;
    if (DisplayMode.getValue(visibility)) {
      displayMode = DisplayMode.getValue(visibility);
    } else if (visibility) {
      displayMode = DisplayMode.FULL;
    } else {
      displayMode = DisplayMode.HIDDEN;
    }
    if (displayMode !== this.fieldDef.visibility.form) {
      this.fieldDef.visibility.form = displayMode;
      this.renderKey++; // notify the components to redraw
    }
  }
}
