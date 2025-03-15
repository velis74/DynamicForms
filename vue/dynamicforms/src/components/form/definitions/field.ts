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
import { Statement } from '../inputs/conditional-visibility';
import { DfForm } from '../namespace';

import RenderParams from './field-render-params';

export default class FormField {
  private declare fieldDef: DfForm.FormFieldJSON;

  public uuid!: string;

  public name!: string;

  public label!: string;

  public placeholder!: string;

  public align!: string;

  public visibility!: DisplayMode;

  public renderParams!: RenderParams;

  public readOnly!: boolean;

  public componentName!: string;

  public helpText!: string;

  public choices!: DfForm.ChoicesJSON[];

  public ajax!: DfForm.AJAXJSON;

  public widthClasses!: string;

  public allowNull!: boolean;

  public renderKey: number;

  public conditionalVisibility!: Statement;

  constructor(fieldDef: DfForm.FormFieldJSON) {
    this.renderKey = 0; // used in row.vue
    // Below we circumvent having to declare an internal variable which property getters would be reading from
    Object.defineProperties(this, {
      fieldDef: { get() { return fieldDef; }, enumerable: false },

      uuid: { get() { return fieldDef.uuid; }, enumerable: true },
      name: { get() { return fieldDef.name; }, enumerable: true },
      label: { get() { return fieldDef.label; }, enumerable: true },
      placeholder: { get() { return fieldDef.placeholder; }, enumerable: true },
      align: {
        get() {
          if (fieldDef.alignment === 'decimal') return 'right';
          return fieldDef.alignment;
        },
        enumerable: true,
      },
      visibility: { get() { return DisplayMode.fromAny(fieldDef.visibility.form); }, enumerable: true },
      renderParams: { get() { return new RenderParams(fieldDef.render_params); }, enumerable: true },
      readOnly: { get() { return fieldDef.read_only === true; }, enumerable: true },
      componentName: {
        get() { return fieldDef.render_params.form_component_name; },
        enumerable: true,
        configurable: true,
      },
      choices: { get() { return fieldDef.choices; }, enumerable: true },
      ajax: { get() { return fieldDef.ajax; }, enumerable: true },
      colspan: { get() { return fieldDef.colspan; }, enumerable: true, configurable: true },
      helpText: { get() { return fieldDef.help_text; }, enumerable: true },
      allowNull: { get() { return fieldDef.allow_null; }, enumerable: true },
      conditionalVisibility: { get() { return fieldDef.conditional_visibility; }, enumerable: true },
    });
  }

  get isVisible() { return (this.visibility !== DisplayMode.SUPPRESS && this.visibility !== DisplayMode.HIDDEN); }

  setVisibility(visibility: number) {
    let displayMode;
    if (DisplayMode.isDefined(visibility)) {
      displayMode = DisplayMode.fromAny(visibility);
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
