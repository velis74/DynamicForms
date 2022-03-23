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
import Vue from 'vue';

import DisplayMode from '../../classes/display_mode';

// Checks if we are in development mode
const IS_DEVELOPMENT = (
  Vue.config.devtools === true || window.webpackHotUpdate || process.env.NODE_ENV === 'development'
);

function wrapInProxy(renderParams) {
  return new Proxy(renderParams, {
    get(target, prop) {
      if (Object.prototype.hasOwnProperty.call(target, prop)) {
        return Reflect.get(...arguments); // eslint-disable-line prefer-rest-params
      }
      if (!(['toJSON', 'constructor', 'render', 'state', '_isVue'].includes(prop) || typeof prop === 'symbol')) {
        // these are called by Vue internals when inspecting in Vue devtools
        console.error(`RenderParams doesn't have property named ${prop.toString()}`);
      }
      return target[prop];
    },
  });
}

function RenderParams(fieldDef) {
  this.inputType = fieldDef.render_params.input_type;
  this.fieldCSSClass = fieldDef.render_params.field_class;
  this.maxLength = fieldDef.render_params.max_length;
  this.allowNull = fieldDef.allow_null;

  // Text input
  this.pattern = fieldDef.render_params.pattern;
  this.min = fieldDef.render_params.min;
  this.max = fieldDef.render_params.max;
  this.minLength = fieldDef.render_params.min_length || 0;
  this.maxLength = fieldDef.render_params.max_length || 1E20;

  // text input, translated into HTML attributes
  this.step = fieldDef.render_params.step;
  this.size = fieldDef.render_params.size;

  // DateTime
  this.formFormat = fieldDef.render_params.form_format;

  // select
  this.multiple = fieldDef.render_params.multiple;
  this.allowTags = fieldDef.render_params.allow_tags;

  return IS_DEVELOPMENT ? wrapInProxy(this) : this;
}

export default class FormField {
  constructor(fieldDef) {
    // Below we circumvent having to declare an internal variable which property getters would be reading from
    Object.defineProperties(this, {
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
      renderParams: { get() { return new RenderParams(fieldDef); }, enumerable: true },
      readOnly: { get() { return fieldDef.read_only === true; }, enumerable: true },
      componentName: { get() { return fieldDef.render_params.form_component_name; }, enumerable: true },
      choices: { get() { return fieldDef.choices; }, enumerable: true },
      widthClasses: { get() { return fieldDef.width_classes; }, enumerable: true },
      helpText: { get() { return fieldDef.help_text; }, enumerable: true },
    });
  }

  get isVisible() { return (this.visibility !== DisplayMode.SUPPRESS && this.visibility !== DisplayMode.HIDDEN); }
}
