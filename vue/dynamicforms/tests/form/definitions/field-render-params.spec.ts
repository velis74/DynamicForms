import RenderParams from '../../../src/components/form/definitions/field-render-params';
import { DfForm } from '../../../src/components/form/namespace';

describe('RenderParams', () => {
  const renderParamsJSON: DfForm.RenderParamsJSON = {
    form_component_def: { detail_url: 'https://example.com/details' },
    form_component_name: 'df-layout',
    input_type: 'text',
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
  };

  it('constructor properly maps fields from DfForm.RenderParamsJSON', () => {
    const renderParams = new RenderParams(renderParamsJSON);

    expect(renderParams.formComponentDef).toEqual(renderParamsJSON.form_component_def);
    expect(renderParams.inputType).toBe(renderParamsJSON.input_type);
    expect(renderParams.fieldCSSClass).toBe(renderParamsJSON.field_class);
    expect(renderParams.pattern).toBe(renderParamsJSON.pattern);
    expect(renderParams.min).toBe(renderParamsJSON.min);
    expect(renderParams.max).toBe(renderParamsJSON.max);
    expect(renderParams.minLength).toBe(renderParamsJSON.min_length);
    expect(renderParams.maxLength).toBe(renderParamsJSON.max_length);
    expect(renderParams.step).toBe(renderParamsJSON.step);
    expect(renderParams.size).toBe(renderParamsJSON.size);
    expect(renderParams.formFormat).toBe(renderParamsJSON.form_format);
    expect(renderParams.multiple).toBe(renderParamsJSON.multiple);
    expect(renderParams.allowTags).toBe(renderParamsJSON.allow_tags);
  });

  it('constructor sets default values for minLength and maxLength when not provided', () => {
    const renderParamsJSONWithoutMinMaxLength: DfForm.RenderParamsJSON = {
      ...renderParamsJSON,
      min_length: undefined,
      max_length: undefined,
    };

    const renderParams = new RenderParams(renderParamsJSONWithoutMinMaxLength);

    expect(renderParams.minLength).toBe(0);
    expect(renderParams.maxLength).toBe(1E20);
  });
});
