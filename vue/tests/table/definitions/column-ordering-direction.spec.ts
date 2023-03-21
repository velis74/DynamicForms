import OrderingDirection from '../../../components/table/definitions/column-ordering-direction';

describe('OrderingDirection', () => {
  // eslint-disable-next-line no-undef
  it('Basic enum checks', () => {
    expect(OrderingDirection.isDefined(OrderingDirection.ASC)).toStrictEqual(true); // isinstance check
    expect(OrderingDirection.ASC).not.toStrictEqual(OrderingDirection.DESC);
    expect(OrderingDirection.ASC).toStrictEqual(OrderingDirection.fromString('asc'));
    expect(OrderingDirection.isDefined(2)).toStrictEqual(true);
    expect(OrderingDirection.isDefined(3)).toStrictEqual(false);
    expect(OrderingDirection[OrderingDirection.ASC]).toStrictEqual('ASC');
  });
});
