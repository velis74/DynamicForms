import DisplayMode from '../../classes/display-mode';
import { DfForm } from '../namespace';

import FormField from './field';
import Operator from './field-operator';
import RenderParams from './field-render-params';

const fieldDef: DfForm.FormFieldJSON = {
  uuid: '123',
  name: 'testName',
  label: 'Test Label',
  placeholder: 'Test Placeholder',
  alignment: 'decimal',
  visibility: {
    table: DisplayMode.SUPPRESS,
    form: DisplayMode.FULL,
  },
  render_params: {
    input_type: 'text',
    form_component_def: { detail_url: 'https://example.com/details' },
    form_component_name: 'TestComponent',
    field_class: 'test-field-class',
    pattern: '^\\d+$',
    min: 1,
    max: 100,
    min_length: 2,
    max_length: 20,
    step: 1,
    size: 10,
    form_format: 'json',
    multiple: false,
    allow_tags: false,
    table: 'df-tablecell-plaintext',
  },
  read_only: true,
  choices: [{ id: 'A', text: 'Choice A' }],
  ajax: {
    url_reverse: 'https://example.com/ajax',
    placeholder: 'Type to search',
    additional_parameters: 'param1=value1&param2=value2',
    query_field: 'search',
  },
  colspan: 'test-width-classes',
  help_text: 'Test Help Text',
  allow_null: true,
  conditional_visibility: ['id', Operator.GT, 12],
};

describe('FormField', () => {
  it('FormField: constructor properly maps fields from DfForm.FormFieldJSON and extra fields', async () => {
    const formField = new FormField(fieldDef);

    // Check if all fields are properly mapped
    expect(formField.uuid).toBe(fieldDef.uuid);
    expect(formField.name).toBe(fieldDef.name);
    expect(formField.label).toBe(fieldDef.label);
    expect(formField.placeholder).toBe(fieldDef.placeholder);
    expect(formField.align).toBe('right');
    expect(formField.visibility).toBe(DisplayMode.FULL);
    expect(formField.renderParams).toBeInstanceOf(RenderParams);
    expect(formField.readOnly).toBe(true);
    expect(formField.componentName).toBe(fieldDef.render_params.form_component_name);
    expect(formField.renderParams.inputType).toBe(fieldDef.render_params.input_type);
    expect(formField.renderParams.formComponentDef).toEqual(fieldDef.render_params.form_component_def);
    expect(formField.renderParams.fieldCSSClass).toBe(fieldDef.render_params.field_class);
    expect(formField.renderParams.pattern).toBe(fieldDef.render_params.pattern);
    expect(formField.renderParams.min).toBe(fieldDef.render_params.min);
    expect(formField.renderParams.max).toBe(fieldDef.render_params.max);
    expect(formField.renderParams.minLength).toBe(fieldDef.render_params.min_length);
    expect(formField.renderParams.maxLength).toBe(fieldDef.render_params.max_length);
    expect(formField.renderParams.step).toBe(fieldDef.render_params.step);
    expect(formField.renderParams.size).toBe(fieldDef.render_params.size);
    expect(formField.renderParams.formFormat).toBe(fieldDef.render_params.form_format);
    expect(formField.renderParams.multiple).toBe(fieldDef.render_params.multiple);
    expect(formField.renderParams.allowTags).toBe(fieldDef.render_params.allow_tags);
    // expect(formField.renderParams.table).toBe(fieldDef.render_params.table); // table member is not mapped
    expect(formField.choices).toBe(fieldDef.choices);
    expect(formField.ajax).toBe(fieldDef.ajax);
    expect(formField.colspan).toBe(fieldDef.colspan);
    expect(formField.helpText).toBe(fieldDef.help_text);
    expect(formField.allowNull).toBe(fieldDef.allow_null);
    expect(formField.conditionalVisibility).toBe(fieldDef.conditional_visibility);

    // Check extra fields
    expect(formField.renderKey).toBe(0);
    expect(formField.isVisible).toBe(true);
  });

  it('FormField: setVisibility properly updates field visibility and increments renderKey', () => {
    const formField = new FormField(fieldDef);

    // Initial state
    expect(formField.visibility).toBe(DisplayMode.FULL);
    expect(formField.renderKey).toBe(0);

    // Update visibility to HIDDEN
    formField.setVisibility(DisplayMode.HIDDEN);
    expect(formField.visibility).toBe(DisplayMode.HIDDEN);
    expect(formField.renderKey).toBe(1);

    // Update visibility to SUPPRESS
    formField.setVisibility(DisplayMode.SUPPRESS);
    expect(formField.visibility).toBe(DisplayMode.SUPPRESS);
    expect(formField.isVisible).toBe(false);
    expect(formField.renderKey).toBe(2);

    // Update visibility to INVISIBLE
    formField.setVisibility(DisplayMode.INVISIBLE);
    expect(formField.visibility).toBe(DisplayMode.INVISIBLE);
    expect(formField.isVisible).toBe(true);
    expect(formField.renderKey).toBe(3);

    // Update visibility to FULL
    formField.setVisibility(DisplayMode.FULL);
    expect(formField.visibility).toBe(DisplayMode.FULL);
    expect(formField.renderKey).toBe(4);

    // Set visibility to an invalid value (should default to HIDDEN because the value is falsy)
    formField.setVisibility(0);
    expect(formField.visibility).toBe(DisplayMode.HIDDEN);
    expect(formField.renderKey).toBe(5);
    expect(formField.isVisible).toBe(false);

    // Set visibility to an invalid value (should default to FULL because the value is truthy)
    formField.setVisibility(-1);
    expect(formField.visibility).toBe(DisplayMode.FULL);
    expect(formField.renderKey).toBe(6);
    expect(formField.isVisible).toBe(true);
  });

  it('FormField: align property maps correctly for different alignment values', () => {
    const alignments = ['left', 'right', 'center', 'decimal'];
    const expectedAlign = ['left', 'right', 'center', 'right'];

    alignments.forEach((alignment, index) => {
      const testFieldDef: DfForm.FormFieldJSON = { ...fieldDef, alignment };
      const formField = new FormField(testFieldDef);
      expect(formField.align).toBe(expectedAlign[index]);
    });
  });
});
