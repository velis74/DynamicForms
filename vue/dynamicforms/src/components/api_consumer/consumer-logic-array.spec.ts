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
  });
});
