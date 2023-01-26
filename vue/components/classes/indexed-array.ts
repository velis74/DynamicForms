/**
 * Indexed array acts like an array, but is actually an object.
 * Some array methods are supported, like .map and .forEach
 * Additionally, the object has members mapping array items by their name for faster access
 *
 * Motivation for theis class is primarily the faster access of array items by their name.
 * The reason this does not extend Array is that Vue seems to redeclare every Array descendant as plain Array
 */
export default class IndexedArray {
  constructor(columns) {
    Object.defineProperties(this, {
      items: { get() { return columns; }, enumerable: false },
      length: { get() { return columns.length; }, enumerable: true },
    });

    this.forEach((item) => { if (item && item.name) { this[item.name] = item; } });
  }

  push(item) {
    this[item.name] = item;
    return this.items.push(item);
  }

  forEach(callback, thisArg) {
    return this.items.forEach(callback, thisArg || this);
  }

  map(callback, thisArg) {
    return this.items.map(callback, thisArg || this);
  }

  reduce(callback, initialValue) {
    return this.items.reduce(callback, initialValue);
  }
}
