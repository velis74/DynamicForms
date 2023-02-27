const OrderingDirection = {
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

export default Object.freeze(OrderingDirection);
