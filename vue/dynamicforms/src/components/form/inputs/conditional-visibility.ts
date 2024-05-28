import Operator from '../definitions/field-operator';
import FormPayload from '../definitions/form-payload';

export type Statement = [ string | Statement, Operator, any | Statement ] | null;

export function XOR(value1: boolean, value2: boolean): boolean {
  return value1 ? !value2 : value2;
}

function calculateVisibility(payload: FormPayload, statement: Statement): boolean {
  if (statement == null) return true;

  const operator = statement[1];

  if (Operator.isLogicOperator(operator)) {
    // we have to go 1 level lower
    switch (statement[1]) {
    case Operator.AND:
      return calculateVisibility(payload, statement[0] as Statement) && calculateVisibility(payload, statement[2]);
    case Operator.OR:
      return calculateVisibility(payload, statement[0] as Statement) || calculateVisibility(payload, statement[2]);
    case Operator.NAND:
      return !(calculateVisibility(payload, statement[0] as Statement) && calculateVisibility(payload, statement[2]));
    case Operator.NOR:
      return !(calculateVisibility(payload, statement[0] as Statement) || calculateVisibility(payload, statement[2]));
    case Operator.XOR:
      return XOR(calculateVisibility(payload, statement[0] as Statement), calculateVisibility(payload, statement[2]));
    case Operator.NOT:
      return !calculateVisibility(payload, statement[0] as Statement);
    default:
      throw new Error(`Not implemented operator ${operator}`);
    }
  } else {
    const fieldValue = payload[statement[0] as string];
    const compareValue = statement[2];
    switch (operator) {
    case Operator.EQUALS:
      return fieldValue === compareValue;
    case Operator.NOT_EQUALS:
      return fieldValue !== compareValue;
    case Operator.LT:
      return fieldValue < compareValue;
    case Operator.LE:
      return fieldValue <= compareValue;
    case Operator.GE:
      return fieldValue >= compareValue;
    case Operator.GT:
      return fieldValue > compareValue;
    case Operator.IN:
      return compareValue?.includes?.(fieldValue) ?? false;
    case Operator.NOT_IN:
      return !(compareValue?.includes?.(fieldValue) ?? true);
    case Operator.INCLUDES:
      return fieldValue?.includes?.(compareValue) ?? false;
    case Operator.NOT_INCLUDES:
      return !(fieldValue?.includes?.(compareValue) ?? true);
    default:
      throw new Error(`Not implemented operator ${operator}`);
    }
  }
}

export default calculateVisibility;
