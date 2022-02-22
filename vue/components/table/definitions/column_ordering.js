import OrderingDirection from './column_ordering_direction';

// This is a really stupid way of telling Vue that the other segments changed as well. It seems to be necessary because
// nothing happened when I did this.orderingArray.splice(...)
const changeCounter = { counter: 0 };

export default class ColumnOrdering {
  /**
   * Column ordering management utility
   *
   * @param orderingString: e.g. ordering asc seg-1
   * @param orderingArray: a common array (created in columns.js) containing all order segments
   * @param column: reference to the column itself. Needed for error messages below
   */
  constructor(orderingString, orderingArray, column) {
    this.direction = OrderingDirection.parseFromOrderingString(orderingString);
    this.changeCounter = changeCounter;
    // First we determine where in the orderingArray we should insert this segment initially
    const ordrIdxMatch = /seg-(\d+)/.exec(orderingString);
    const initialSegment = ordrIdxMatch != null ? Number(ordrIdxMatch[1]) : 0;
    orderingArray.length = Math.max(orderingArray.length, initialSegment);
    if (initialSegment) orderingArray.splice(initialSegment - 1, 1, this);

    Object.defineProperties(this, {
      column: { get() { return column; }, enumerable: false },
      orderingArray: { get() { return orderingArray; }, enumerable: false },
      isOrderable: { get() { return orderingString.includes('ordering'); }, enumerable: true },
      isOrdered: { get() { return this.isOrderable && (this.segment > 0); }, enumerable: true },
      segment: { get() { return (this.isOrderable && orderingArray.indexOf(this) + 1) || null; }, enumerable: true },
    });
  }

  /**
   * cycles field ordering 'asc' -> 'desc' -> 'unsorted'
   */
  cycleOrdering() {
    if (!this.isOrdered) {
      this.direction = OrderingDirection.ASC;
    } else if (this.direction === OrderingDirection.ASC) {
      this.direction = OrderingDirection.DESC;
    } else {
      this.direction = OrderingDirection.UNORDERED;
    }
  }

  /**
   * sets column sort sequence and direction
   * @param direction: one of "asc", "desc" or "unsorted"
   * @param sequence: integer. if none is provided, existing sequence # will be used
   * or 1 if column was unsorted
   */
  setSorted(direction, sequence) {
    let seq = sequence || (this.segment > 0 ? this.segment : 1);
    if (seq > this.orderingArray.length + 1) seq = this.orderingArray.length + 1;
    if (!this.isOrderable) {
      throw new Error(`column ${this.column.name} is not orderable, but you are trying to set its order direction.`);
    } else if (OrderingDirection.isDefined(direction)) {
      if (this.segment) this.orderingArray.splice(this.segment - 1, 1);
      if (direction !== OrderingDirection.UNORDERED) this.orderingArray.splice(seq - 1, 0, this);
      this.direction = direction;
    } else {
      console.warn(`unknown sort direction "${direction}" for the column ${this.column.name}. not doing anything`);
    }
  }

  handleColumnHeaderClick(event) {
    if (!this.isOrderable) return; // don't do anything if this column is not sortable
    // const prevOrdering = [...this.orderingArray];

    if (event.altKey) {
      // Show dialog with sort order options
    } else if (event.ctrlKey && event.shiftKey) {
      // remove column from ordering
      this.setSorted(OrderingDirection.UNORDERED);
    } else if (event.ctrlKey) {
      // set column as first sorted column
      this.setSorted(this.direction === OrderingDirection.ASC ? OrderingDirection.DESC : OrderingDirection.ASC, 1);
    } else if (event.shiftKey) {
      // Change segment sort direction (and add it to sort segments list if not already there)
      // if shift is pressed add segment to existing ones.
      const ordrIdx = this.segment;
      const oSeq = ordrIdx || this.orderingArray.length + 1;
      const oDir = this.direction === OrderingDirection.ASC ? OrderingDirection.DESC : OrderingDirection.ASC;
      this.setSorted(oDir, oSeq);
    } else {
      this.cycleOrdering();
      this.orderingArray.splice(0, this.orderingArray.length);
      this.setSorted(this.direction, 1);
    }
    changeCounter.counter++;
  }

  calculateOrderingValue(transformationFunction) {
    // this method should be in TableColumns, but it seems Vue regenerates any array derivative to plain array
    const cols = this.orderingArray.map((columnOrdering) => (
      { name: columnOrdering.column.name, direction: columnOrdering.direction }
    ));
    if (transformationFunction) return transformationFunction(cols);
    return cols.map((o) => (o.direction === OrderingDirection.ASC ? '' : '-') + o.name);
  }
}
