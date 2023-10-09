import ConsumerLogicArray from './consumer-logic-array';
import uxData from './consumer-logic-array.spec.json';
import ConsumerLogicBase from './consumer-logic-base';

describe('aRrAy', () => {
  it('Creating', () => {
    const consumer = new ConsumerLogicArray(uxData, []);
    expect(consumer).not.toBeUndefined();
    expectTypeOf(consumer).toMatchTypeOf(ConsumerLogicBase);
  });

  it('Filtering', async () => {
    const consumer = new ConsumerLogicArray(uxData, []);
    const filterData = { id: 1 };
    // TODO: currently filtering is not enabled on array consumer, remove after it is implemented (if)
    await expect(consumer.filter(filterData)).rejects.toThrowError();
    expect(consumer.filterData).toEqual(filterData);

    const displayFilterData = { 'before-display': 1, before: 2, 'type-display': 1 };
    await expect(consumer.filter(displayFilterData)).rejects.toThrowError();
    expect(consumer.filterData).toEqual(
      Object.fromEntries(Object.entries(displayFilterData).filter(([key]) => !key.endsWith('-display'))),
    );

    const nullFilterData = { a: null, b: undefined, c: 1, d: { e: 2 } };
    await expect(consumer.filter(nullFilterData)).rejects.toThrowError();
    expect(consumer.filterData).toEqual(
      Object.fromEntries(Object.entries(nullFilterData).filter(([, value]) => !!value)),
    );
  });
});
