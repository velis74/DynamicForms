import OrderingDirection from './column-ordering-direction';

describe('OrderingDirection', () => {
  // eslint-disable-next-line no-undef
  it('Basic enum checks', () => {
    expect(OrderingDirection.isDefined(OrderingDirection.ASC)).toStrictEqual(true); // isinstance check
    expect(OrderingDirection.ASC).not.toStrictEqual(OrderingDirection.DESC);
    expect(OrderingDirection.ASC).toStrictEqual(OrderingDirection.fromString('asc'));
    expect(OrderingDirection.isDefined(2)).toStrictEqual(true);
    expect(OrderingDirection.isDefined(3)).toStrictEqual(false);
    expect(OrderingDirection[OrderingDirection.ASC]).toStrictEqual('ASC');
    expect(OrderingDirection.fromString('asc')).toStrictEqual(OrderingDirection.ASC);
    expect(OrderingDirection.fromString('ASC')).toStrictEqual(OrderingDirection.ASC);
    expect(OrderingDirection.fromString('desc')).toStrictEqual(OrderingDirection.DESC);
    expect(OrderingDirection.fromString('a')).toStrictEqual(OrderingDirection.UNORDERED);
  });
});
