import Enum from 'enum';

const OrderingDirection = new Enum({
  ASC: 1,
  DESC: 2,
  UNORDERED: 0,
});

OrderingDirection.parseFromOrderingString = function parseFromOrderingString(ordering) {
  if (ordering.includes('asc')) return OrderingDirection.ASC;
  if (ordering.includes('desc')) return OrderingDirection.DESC;
  return OrderingDirection.UNORDERED;
};

export default Object.freeze(OrderingDirection);
