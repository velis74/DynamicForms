/**
 * Indexed array acts like an array, but is actually an object.
 * Some array methods are supported, like .map and .forEach
 * Additionally, the object has members mapping array items by their name for faster access
 *
 * Motivation for this class is primarily the faster access of array items by their name.
 * The reason this does not extend Array is that Vue seems to redeclare every Array descendant as plain Array
 */
interface ItemWithName {name: string;}

export default class IndexedArray<IndexedItem extends ItemWithName> {
  items!: IndexedItem[];

  length!: number;

  // [key: string]: IndexedItem;

  constructor(columns: IndexedItem[]) {
    Object.defineProperties(this, {
      items: { get() { return columns; }, enumerable: false },
      length: { get() { return columns.length; }, enumerable: true },
    });

    this.forEach((item: IndexedItem) => { if (item && item.name) { this[item.name] = item; } });
  }

  push(item: IndexedItem) {
    this[item.name] = item;
    return this.items.push(item);
  }

  forEach(
    callback: (value: IndexedItem, index?: number, array?: IndexedItem[]) => void,
    thisArg?: IndexedArray<IndexedItem>,
  ) {
    return this.items.forEach(callback, thisArg || this);
  }

  map(
    callback: (value: IndexedItem, index?: number, array?: IndexedItem[]) => void,
    thisArg?: IndexedArray<IndexedItem>,
  ) {
    return this.items.map(callback, thisArg || this);
  }

  reduce(
    callback: (previousValue: any, currentValue: IndexedItem, currentIndex: number, array: IndexedItem[]) => any,
    initialValue?: any,
  ) {
    return this.items.reduce(callback, initialValue);
  }
}
