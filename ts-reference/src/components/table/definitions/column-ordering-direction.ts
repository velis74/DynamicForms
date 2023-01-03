enum OrderingDirection {
  ASC = 1,
  DESC = 2,
  UNORDERED = 0,
}

export function parseFromOrderingString(ordering: string | OrderingDirection): OrderingDirection {
  if (ordering in OrderingDirection) {
    // @ts-ignore
    return OrderingDirection[ordering];
  }
  return OrderingDirection.UNORDERED;
}

export default OrderingDirection;
