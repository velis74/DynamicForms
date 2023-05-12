enum OrderingDirection {
  ASC = 1 as number,
  DESC = 2 as number,
  UNORDERED = 0 as number,
}

namespace OrderingDirection {
  export function fromString(ordering: string) {
    if (ordering.toLowerCase().includes('asc')) return OrderingDirection.ASC;
    if (ordering.toLowerCase().includes('desc')) return OrderingDirection.DESC;
    return OrderingDirection.UNORDERED;
  }

  export function isDefined(ordering: number) {
    return Object.values(OrderingDirection).includes(ordering);
  }
}

/*
const OrderingDirection1 = {
  ASC: 1 as number,
  DESC: 2 as number,
  UNORDERED: 0 as number,

  fromString(ordering: string) {
    if (ordering.includes('asc')) return OrderingDirection.ASC;
    if (ordering.includes('desc')) return OrderingDirection.DESC;
    return OrderingDirection.UNORDERED;
  },

  isDefined(ordering: number) {
    const allValues = [this.ASC, this.DESC, this.UNORDERED];
    return allValues.includes(ordering);
  },
} as const;
*/

Object.freeze(OrderingDirection);
export default OrderingDirection;
