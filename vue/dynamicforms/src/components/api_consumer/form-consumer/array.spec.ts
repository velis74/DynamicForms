import { reactive, ref } from 'vue';

import FormConsumerArray from './array';
import ux_def from './array.spec.json';

describe('Form Consumer Array', () => {
  it('Create', () => {
    const consumer = new FormConsumerArray({
      definition: ux_def,
      data: reactive([]),
      pk: ref(1),
      pkName: 'id',
    });

    expectTypeOf(consumer).toEqualTypeOf<FormConsumerArray>();
  });

  it('Get Definition, PK and Record', async () => {
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
    const consumer = new FormConsumerArray({
      definition: ux_def,
      data: internalData,
      pk: ref(1),
      pkName: 'id',
    });

    const definition = await consumer.getUXDefinition();
    expect(definition).not.toBeUndefined();
    expect(definition.payload).not.toBeUndefined();

    const record = (await consumer.getRecord())!;
    expect(consumer.pkValue).not.toBeUndefined();
    expect(definition.payload[definition.pkName]).toBe(record[definition.pkName]);
    expect(record[definition.pkName]).not.toBeUndefined();
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
    const consumer = new FormConsumerArray({
      definition: ux_def,
      data: internalData,
      pk: ref(1),
      pkName: 'id',
    });
    await consumer.getUXDefinition();
    consumer.data!.code = 'bbc';
    await consumer.save();

    let record = (await consumer.getRecord())!;

    expect(record).not.toBeUndefined();
    expect(record.code).toBe('bbc');

    expect(consumer.data).not.toBeUndefined();

    const savingData = Object.fromEntries(Object.entries(internalData[0]).filter(([key]) => key !== consumer.pkName));
    consumer.data = savingData;
    await consumer.save();

    record = internalData.find((element) => element[consumer.pkName] === -1);
    expect(record).not.toBeUndefined();
    expect(record).toEqual(savingData);
  });

  it('Deleting a record', async () => {
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
    const pk = ref<string | number>(1);
    const consumer = new FormConsumerArray({
      definition: ux_def,
      data: internalData,
      pk,
      pkName: 'id',
    });

    let definition = await consumer.getUXDefinition();
    await consumer.delete();

    expect(internalData).toHaveLength(2);
    expect(internalData.filter((element) => element[definition.pkName] === pk.value));

    pk.value = 'new';
    definition = await consumer.getUXDefinition();

    await expect(consumer.delete).rejects.toThrow();
  });
});
