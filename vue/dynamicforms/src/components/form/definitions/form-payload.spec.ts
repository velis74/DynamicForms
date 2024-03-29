import DisplayMode from '../../classes/display-mode';

import FormPayload from './form-payload';
import FormLayout from './layout';

const fieldValues = {
  fieldWritable: 12,
  fieldReadOnly: 'abc',
};

const fieldDefinitions = {
  fields: {
    fieldWritable: {
      name: 'fieldWritable',
      read_only: false,
      visibility: { form: DisplayMode.FULL },
    },
    fieldReadOnly: {
      name: 'fieldReadOnly',
      read_only: true,
      visibility: { form: DisplayMode.FULL },
    },
    fieldHidden: {
      name: 'fieldHidden',
      read_only: true,
      visibility: { form: DisplayMode.SUPPRESS },
    },
  },
  rows: [],
  componentName: null,
  fieldName: null,
};

describe('FormPayload', () => {
  it('Check if calling constructor without parameters produces an empty FormPayload', () => {
    const ds = FormPayload.create();
    expect(Object.keys(ds).length).toEqual(0);
  });
  it('Check if a basic data sample parses and properly sets up the fields', () => {
    const formLayout = new FormLayout(fieldDefinitions);
    const ds = FormPayload.create(fieldValues, formLayout);

    expect(ds.fieldWritable).toEqual(12);
    expect(ds.fieldReadOnly).toEqual('abc');
    expect(ds.fieldHidden).toBeUndefined();
    expect(ds['$extra-data']).toEqual({});

    ds.fieldWritable += 1;
    expect(ds.fieldWritable).toEqual(13);

    const invalidSet = () => { ds.fieldReadOnly = 'huj'; };
    expect(invalidSet).toThrow(TypeError);
  });
  it('Check if cloning actually creates two separate and completely unlinked instances', () => {
    const ds1 = FormPayload.create(fieldValues, new FormLayout(fieldDefinitions));
    const ds2 = FormPayload.create(ds1);

    expect(ds2.fieldWritable).toEqual(12);
    expect(ds2.fieldReadOnly).toEqual('abc');
    expect(ds2.fieldHidden).toBeUndefined();
    expect(ds2['$extra-data']).toEqual({});

    ds1.fieldWritable += 1;
    expect(ds1.fieldWritable).toEqual(13);
    expect(ds2.fieldWritable).toEqual(12);

    ds1.addExtraData({ newValue: 5 });
    expect(ds2['$extra-data']).toEqual({});
    expect(ds1['$extra-data']).toEqual({ newValue: 5 });

    ds2.fieldWritable += 5;
    expect(ds1.fieldWritable).toEqual(13);
    expect(ds2.fieldWritable).toEqual(17);
  });
});
