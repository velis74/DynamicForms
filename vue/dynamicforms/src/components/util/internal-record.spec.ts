import { reactive } from 'vue';

import createInternalRecord, { toExternalRecordCopy } from './internal-record';

const data = reactive({ prop1: 'hello', prop2: 'world' });

describe('Internal Record', () => {
  it('Create Internal Record', () => {
    const result = createInternalRecord(data, 'id', -1);
    expect(result).not.toBeUndefined();
    // eslint-disable-next-line no-underscore-dangle
    expect(result.__pk_name).toEqual('id');
    expect(result.id).toEqual(-1);

    result.id = -2;
    expect(result.id).toEqual(-1);
  });

  it('Changing Primary Key Property Does Not Effect Original', () => {
    const result = createInternalRecord(data, 'prop1', 'bye');

    expect(result).not.toBeUndefined();
    expect(result.prop1).toBe('hello');
    expect(result.prop2).toBe('world');

    expect(data.prop1).toBe('hello');
    expect(data.prop2).toBe('world');

    result.prop1 = 'nice';
    expect(result.prop1).toBe('hello');
    expect(data.prop1).toBe('hello');

    result.prop2 = 'time';
    expect(result.prop2).toBe('time');
    expect(data.prop2).toBe('time');
  });

  it('Internal and back to external', () => {
    const result = toExternalRecordCopy(createInternalRecord(data, 'id', -1));

    expect(result).not.toBeUndefined();
    const resultWithoutPk = Object.fromEntries(Object.entries(result).filter(([key]) => key !== 'id'));
    expect(resultWithoutPk).toEqual(data);
  });
});
