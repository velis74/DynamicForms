import IndexedArray, { ItemWithName } from './indexed-array';

describe('IndexedArray', () => {
  it('should be initialized with correct items and length properties', () => {
    const items: ItemWithName[] = [
      { name: 'item1' },
      { name: 'item2' },
      { name: 'item3' },
    ];
    const indexedArray = new IndexedArray(items);

    expect(indexedArray.items).toEqual(items);
    expect(indexedArray.length).toEqual(items.length);
  });

  it('should support item insertion and deletion', () => {
    const items: ItemWithName[] = [
      { name: 'item1' },
      { name: 'item2' },
      { name: 'item3' },
    ];
    const indexedArray = new IndexedArray(items);

    const newItem: ItemWithName = { name: 'item4' };

    // Insert item
    indexedArray.push(newItem);

    expect(indexedArray.length).toEqual(4);
    expect(indexedArray[newItem.name]).toEqual(newItem);
  });

  it('map: should return a new array with the mapped items', () => {
    const items: ItemWithName[] = [
      { name: 'item1' },
      { name: 'item2' },
      { name: 'item3' },
    ];

    const indexedArray = new IndexedArray(items);
    const result = indexedArray.map((item) => item.name);
    expect(result).toEqual(['item1', 'item2', 'item3']);
  });

  it('should reduce the array to a single value', () => {
    const items: ItemWithName[] = [
      { name: 'item1' },
      { name: 'item2' },
      { name: 'item3' },
    ];

    const indexedArray = new IndexedArray(items);
    const result = indexedArray.reduce(
      (previousValue: string, currentValue: ItemWithName) => previousValue + currentValue.name,
      '',
    );

    expect(result).toEqual('item1item2item3');
  });
});
