import Operator, { defaultOperator } from '../../../src/components/form/definitions/field-operator';

describe('Operator', () => {
  it('Create Operators From String', () => {
    expect(Operator.fromString('NOT')).toBe(Operator.NOT);
    expect(Operator.fromString('OR')).toBe(Operator.OR);
    expect(Operator.fromString('AND')).toBe(Operator.AND);
    expect(Operator.fromString('XOR')).toBe(Operator.XOR);
    expect(Operator.fromString('NAND')).toBe(Operator.NAND);
    expect(Operator.fromString('NOR')).toBe(Operator.NOR);

    expect(Operator.fromString('EQUALS')).toBe(Operator.EQUALS);
    expect(Operator.fromString('NOT_EQUALS')).toBe(Operator.NOT_EQUALS);
    expect(Operator.fromString('GT')).toBe(Operator.GT);
    expect(Operator.fromString('LT')).toBe(Operator.LT);
    expect(Operator.fromString('GE')).toBe(Operator.GE);
    expect(Operator.fromString('LE')).toBe(Operator.LE);
    expect(Operator.fromString('IN')).toBe(Operator.IN);
    expect(Operator.fromString('NOT_IN')).toBe(Operator.NOT_IN);

    expect(Operator.fromString('THIS WILL NEVER BE AN OPERATOR')).toBe(defaultOperator);
  });
  it('Create Operators From Any', () => {
    expect(Operator.fromAny(Operator.AND)).toBe(Operator.AND);
    expect(Operator.fromAny('AND')).toBe(Operator.AND);
    expect(Operator.fromAny('AND')).toBe(Operator.fromAny(Operator.AND));

    expect(Operator.fromAny(100)).toBe(defaultOperator);
    expect(Operator.fromString('THIS WILL NEVER BE AN OPERATOR')).toBe(defaultOperator);
  });
  it('Check If Defined', () => {
    expect(Operator.isDefined(100)).toBe(false);
    expect(Operator.isDefined('AND')).toBe(true);
    expect(Operator.isDefined('THIS WILL NEVER BE AN OPERATOR')).toBe(true);
  });
  it('Check If Operator Is Logic Operator', () => {
    expect(Operator.isLogicOperator(Operator.AND)).toBe(true);
    expect(Operator.isLogicOperator(Operator.EQUALS)).toBe(false);

    expect(Operator.isLogicOperator(100)).toBe(true);
    expect(Operator.isLogicOperator(-100)).toBe(false);
  });
});
