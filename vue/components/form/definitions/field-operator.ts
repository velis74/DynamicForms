/**
 * Operators provides us a functionality for backend to send us complex condition upon which we send
 * dynamic visibility prop for form input fields
 */
enum Operator {
  // Logic Operators
  NOT = 0,
  OR = 1,
  AND = 2,
  XOR = 3,
  NAND = 4,
  NOR = 5,

  // Comparators (comparison operators)
  EQUALS = -1,
  NOT_EQUALS = -2,
  GT = -3,
  LT = -4,
  GE = -5,
  LE = -6,
  INCLUDED = -7,
}

namespace Operator {
  export function fromString(operator: string): Operator {
    if (operator.toUpperCase() === 'NOT') return Operator.NOT;
    if (operator.toUpperCase() === 'OR') return Operator.OR;
    if (operator.toUpperCase() === 'AND') return Operator.AND;
    if (operator.toUpperCase() === 'XOR') return Operator.XOR;
    if (operator.toUpperCase() === 'NAND') return Operator.NAND;
    if (operator.toUpperCase() === 'NOR') return Operator.NOR;

    if (operator.toUpperCase() === 'EQUALS') return Operator.EQUALS;
    if (operator.toUpperCase() === 'NOT_EQUALS') return Operator.NOT_EQUALS;
    if (operator.toUpperCase() === 'GT') return Operator.GT;
    if (operator.toUpperCase() === 'LT') return Operator.LT;
    if (operator.toUpperCase() === 'GE') return Operator.GE;
    if (operator.toUpperCase() === 'LE') return Operator.LE;
    if (operator.toUpperCase() === 'INCLUDES') return Operator.INCLUDED;
    return Operator.AND;
  }

  export function fromAny(mode: any): Operator {
    const input = (typeof mode === 'number') ? mode : Operator.fromString(mode as string);
    if (Object.values(Operator).includes(input)) return input;
    return Operator.AND;
  }

  export function isDefined(operator: number | string): boolean {
    const check = (typeof operator === 'number') ? operator : Operator.fromString(operator as string);
    return Object.values(Operator).includes(check);
  }

  export function isLogicOperator(operator: any): boolean {
    return operator >= 0;
  }
}

Object.freeze(Operator);

export default Operator;
