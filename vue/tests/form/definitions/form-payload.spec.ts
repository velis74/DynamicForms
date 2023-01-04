import ColumnDisplay from '../../../components/classes/display-mode';
import FormPayload from '../../../components/form/definitions/form-payload';
import FormLayout from '../../../components/form/definitions/layout';

const fieldValues = {
  fieldWritable: 12,
  fieldReadOnly: 'abc',
};

const fieldDefinitions = {
  fields: {
    fieldWritable: {
      name: 'fieldWritable',
      read_only: false,
      visibility: { form: ColumnDisplay.FULL },
    },
    fieldReadOnly: {
      name: 'fieldReadOnly',
      read_only: true,
      visibility: { form: ColumnDisplay.FULL },
    },
    fieldHidden: {
      name: 'fieldHidden',
      read_only: true,
      visibility: { form: ColumnDisplay.SUPPRESS },
    },
  },
  rows: [],
  componentName: null,
  fieldName: null,
};

describe('FormPayload', () => {
  // eslint-disable-next-line no-undef
  it('Check if a basic data sample parses and properly sets up the fields', () => {
    const ds = new FormPayload(fieldValues, new FormLayout(fieldDefinitions));

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
    const ds1 = new FormPayload(fieldValues, new FormLayout(fieldDefinitions));
    const ds2 = new FormPayload(ds1);

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
