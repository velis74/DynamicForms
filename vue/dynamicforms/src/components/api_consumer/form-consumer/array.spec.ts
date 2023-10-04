import { reactive } from 'vue';

import FormConsumerArray from './array';
import ux_def from './array.spec.json';

describe('Form Consumer Array', () => {
  it('Create', () => {
    const consumer = new FormConsumerArray({ definition: ux_def, data: reactive([]) });

    expectTypeOf(consumer).toEqualTypeOf<FormConsumerArray>();
  });

  it('Get Definition, PK and Record', () => {
    const consumer = new FormConsumerArray({ definition: ux_def, data: reactive([]) });

    const definition = consumer.getUXDefinition();
    expect(definition).not.toBeUndefined();
    expect(definition.payload).not.toBeUndefined();

    expect(definition.payload).toEqual(consumer.getRecord());

    expect(consumer.pkValue).not.toBeUndefined();
    expect(definition.payload[definition.primary_key_name]).toBe(consumer.getRecord()[definition.primary_key_name]);
    expect(consumer.getRecord()[definition.primary_key_name]).toBeUndefined();
  });

  it('Internal Records', async () => {
    const internalData = reactive([
      {
        id: 1,
        item_type: 0,
        code: 'abc12345',
        enabled: true,
        amount: 5,
        item_flags: 'A',
        comment: 'gfgdfgfdgd213',
      },
      {
        id: 2,
        item_type: 1,
        code: 'abc12',
        enabled: true,
        amount: 5,
        item_flags: 'A',
        comment: 'gfgd',
      },
      {
        id: 3,
        item_type: 2,
        code: 'abc',
        enabled: true,
        amount: 5,
        item_flags: 'A',
        comment: '',
      },
    ]);

    const consumer = new FormConsumerArray({ definition: ux_def, data: internalData });
    consumer.getUXDefinition();
    let internalRecord = consumer.getInternalRecord(consumer.pkValue);

    expect(internalRecord).not.toBeUndefined();
    expect(internalRecord[consumer.pkName]).toBe(consumer.pkValue);
    expect(
      Object.fromEntries(Object.entries(internalRecord).filter(([key]) => key !== consumer.pkName)),
    ).toEqual(consumer.getRecord());

    await consumer.delete();
    internalRecord = consumer.getInternalRecord(consumer.pkValue);
    expect(internalRecord).toBeUndefined();

    expect(
      internalData.find((element) => element[consumer.pkName] === consumer.pkValue),
    ).toBeUndefined();
  });

  it('Saving new records', async () => {
    const internalData = reactive([
      {
        id: 1,
        item_type: 0,
        code: 'abc12345',
        enabled: true,
        amount: 5,
        item_flags: 'A',
        comment: 'gfgdfgfdgd213',
      },
      {
        id: 2,
        item_type: 1,
        code: 'abc12',
        enabled: true,
        amount: 5,
        item_flags: 'A',
        comment: 'gfgd',
      },
      {
        id: 3,
        item_type: 2,
        code: 'abc',
        enabled: true,
        amount: 5,
        item_flags: 'A',
        comment: '',
      },
    ]);
    const consumer = new FormConsumerArray({ definition: ux_def, data: internalData });
    consumer.getUXDefinition();
    consumer.data.code = 'bbc';
    await consumer.save();

    let internalRecord = consumer.getInternalRecord(consumer.pkValue);

    expect(internalRecord).not.toBeUndefined();
    expect(internalRecord.code).toBe('bbc');

    const savingData = Object.fromEntries(Object.entries(internalData[0]).filter(([key]) => key !== consumer.pkName));
    consumer.data = savingData;
    await consumer.save();

    internalRecord = internalData.find((element) => element[consumer.pkName] === -1);
    expect(internalRecord).not.toBeUndefined();
    expect(internalRecord).toEqual(savingData);
  });
});
