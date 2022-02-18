export default class IndexedColumns {
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
