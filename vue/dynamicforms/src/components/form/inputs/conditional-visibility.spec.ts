import _ from 'lodash';

import DisplayMode from '../../classes/display-mode';
import Operator from '../definitions/field-operator';
import FormPayload from '../definitions/form-payload';
import FormLayout from '../definitions/layout';
// eslint-disable-next-line import/no-named-as-default
import DfForm from '../namespace';

import calculateVisibility, { Statement, XOR } from './conditional-visibility';

type FieldValues = { [key: string]: any };

/** Field values to emulate FormPayload we get from API (or RAM) */
const fieldValues: FieldValues = {
  conditionedField: 'I disappear',
  numberCondition: 5,
  arrayCondition: ['a', 'b', 'c'],
  stringCondition: 'appear',
};

type FieldDefinitions = { fields: { [key: string]: any }, rows?: any[], componentName?: null, fieldName?: null };

/** Emulates fields definitions we get from API (or RAM) */
const fieldDefinitions: FieldDefinitions = {
  fields: {
    conditionedField: {
      name: 'conditionedField',
      read_only: false,
      visibility: { form: DisplayMode.FULL },
    },
    numberCondition: {
      name: 'numberCondition',
      read_only: false,
      visibility: { form: DisplayMode.FULL },
    },
    arrayCondition: {
      name: 'arrayCondition',
      read_only: false,
      visibility: { form: DisplayMode.FULL },
    },
    stringCondition: {
      name: 'stringCondition',
      read_only: false,
      visibility: { form: DisplayMode.FULL },
    },
  },
  rows: [],
  componentName: null,
  fieldName: null,
};

type ConditionPair = { truth: Statement[], lie: Statement[] };
type TypeConditions = { [key: string]: ConditionPair };

/** Utilities for testing with number conditions */
const numberValues = {
  lower: fieldValues.numberCondition - 6,
  equal: fieldValues.numberCondition,
  higher: fieldValues.numberCondition + 6,
};

const stringValues = {
  equal: fieldValues.stringCondition,
  not_equal: `${fieldValues.stringCondition} false`,
};

const stringSubstring = {
  substring: `${fieldValues.stringCondition.substring(0, 3)}`,
  random: 'ungaboongaboong',
};

const getNumberCondition = (
  operator: Operator,
  value: number | number[],
): Statement => ['numberCondition', operator, value];
const getStringCondition = (
  operator: Operator,
  value: string | string[],
): Statement => ['stringCondition', operator, value];
const getCompositeCondition =
  (conditionA: Statement, operator: Operator, conditionB?: Statement): Statement => (
    [conditionA, operator, conditionB]
  );

const conditions: { [key: string]: TypeConditions } = {
  numberConditions: {
    equals: {
      truth: [getNumberCondition(Operator.EQUALS, numberValues.equal)],
      lie: [
        getNumberCondition(Operator.EQUALS, numberValues.lower),
        getNumberCondition(Operator.EQUALS, numberValues.higher),
      ],
    } as ConditionPair,
    notEquals: {
      truth: [
        getNumberCondition(Operator.NOT_EQUALS, numberValues.lower),
        getNumberCondition(Operator.NOT_EQUALS, numberValues.higher),
      ],
      lie: [getNumberCondition(Operator.NOT_EQUALS, numberValues.equal)],
    } as ConditionPair,
    lower: {
      truth: [getNumberCondition(Operator.LT, numberValues.higher)],
      lie: [
        getNumberCondition(Operator.LT, numberValues.equal),
        getNumberCondition(Operator.LT, numberValues.lower),
      ],
    } as ConditionPair,
    greater: {
      truth: [getNumberCondition(Operator.GT, numberValues.lower)],
      lie: [
        getNumberCondition(Operator.GT, numberValues.equal),
        getNumberCondition(Operator.GT, numberValues.higher),
      ],
    } as ConditionPair,
    lowerEqual: {
      truth: [
        getNumberCondition(Operator.LE, numberValues.higher),
        getNumberCondition(Operator.LE, numberValues.equal),
      ],
      lie: [
        getNumberCondition(Operator.LE, numberValues.lower),
      ],
    } as ConditionPair,
    greaterEqual: {
      truth: [
        getNumberCondition(Operator.GE, numberValues.lower),
        getNumberCondition(Operator.GE, numberValues.equal),
      ],
      lie: [
        getNumberCondition(Operator.GE, numberValues.higher),
      ],
    } as ConditionPair,
    in: {
      truth: [
        getNumberCondition(Operator.IN, [numberValues.equal]),
        getNumberCondition(Operator.IN, [numberValues.equal, numberValues.higher]),
        getNumberCondition(Operator.IN, [numberValues.equal, numberValues.lower]),
        getNumberCondition(Operator.IN, [numberValues.equal, numberValues.higher, numberValues.lower]),
      ],
      lie: [
        getNumberCondition(Operator.IN, [numberValues.higher, numberValues.lower]),
        getNumberCondition(Operator.IN, [numberValues.higher]),
        getNumberCondition(Operator.IN, [numberValues.lower]),
      ],
    } as ConditionPair,
    not_in: {
      truth: [
        getNumberCondition(Operator.NOT_IN, [numberValues.higher, numberValues.lower]),
        getNumberCondition(Operator.NOT_IN, [numberValues.higher]),
        getNumberCondition(Operator.NOT_IN, [numberValues.lower]),
      ],
      lie: [
        getNumberCondition(Operator.NOT_IN, [numberValues.equal]),
        getNumberCondition(Operator.NOT_IN, [numberValues.equal, numberValues.higher]),
        getNumberCondition(Operator.NOT_IN, [numberValues.equal, numberValues.lower]),
        getNumberCondition(Operator.NOT_IN, [numberValues.equal, numberValues.higher, numberValues.lower]),
      ],
    } as ConditionPair,
  } as TypeConditions,
  stringConditions: {
    equals: {
      truth: [
        getStringCondition(Operator.EQUALS, stringValues.equal),
      ],
      lie: [
        getStringCondition(Operator.EQUALS, stringValues.not_equal),
      ],
    } as ConditionPair,
    notEquals: {
      truth: [
        getStringCondition(Operator.NOT_EQUALS, stringValues.not_equal),
      ],
      lie: [
        getStringCondition(Operator.NOT_EQUALS, stringValues.equal),
      ],
    } as ConditionPair,
    in: {
      truth: [
        getStringCondition(Operator.IN, [stringValues.equal]),
        getStringCondition(Operator.IN, [stringValues.equal, stringValues.not_equal]),
      ],
      lie: [
        getStringCondition(Operator.IN, [stringValues.not_equal]),
      ],
    } as ConditionPair,
    not_in: {
      truth: [
        getStringCondition(Operator.NOT_IN, [stringValues.not_equal]),
      ],
      lie: [
        getStringCondition(Operator.NOT_IN, [stringValues.equal]),
        getStringCondition(Operator.NOT_IN, [stringValues.equal, stringValues.not_equal]),
      ],
    } as ConditionPair,
    includes: {
      truth: [
        getStringCondition(Operator.INCLUDES, stringSubstring.substring),
      ],
      lie: [
        getStringCondition(Operator.INCLUDES, stringSubstring.random),
      ],
    } as ConditionPair,
    not_includes: {
      truth: [
        getStringCondition(Operator.NOT_INCLUDES, stringSubstring.random),
      ],
      lie: [
        getStringCondition(Operator.NOT_INCLUDES, stringSubstring.substring),
      ],
    } as ConditionPair,
  } as TypeConditions,
  nullConditions: {
    noCondition: {
      truth: [null as Statement],
      lie: [],
    },
  },
  compositeConditions: {
    and: {
      truth: [
        getCompositeCondition(
          getNumberCondition(Operator.EQUALS, numberValues.equal),
          Operator.AND,
          getStringCondition(Operator.EQUALS, stringValues.equal),
        ),
      ],
      lie: [
        getCompositeCondition(
          getNumberCondition(Operator.EQUALS, numberValues.lower),
          Operator.AND,
          getStringCondition(Operator.EQUALS, stringValues.equal),
        ),
        getCompositeCondition(
          getNumberCondition(Operator.EQUALS, numberValues.equal),
          Operator.AND,
          getStringCondition(Operator.EQUALS, stringValues.not_equal),
        ),
        getCompositeCondition(
          getNumberCondition(Operator.EQUALS, numberValues.lower),
          Operator.AND,
          getStringCondition(Operator.EQUALS, stringValues.not_equal),
        ),
      ],
    },
    or: {
      truth: [
        getCompositeCondition(
          getNumberCondition(Operator.EQUALS, numberValues.equal),
          Operator.OR,
          getStringCondition(Operator.EQUALS, stringValues.equal),
        ),
        getCompositeCondition(
          getNumberCondition(Operator.EQUALS, numberValues.lower),
          Operator.OR,
          getStringCondition(Operator.EQUALS, stringValues.equal),
        ),
        getCompositeCondition(
          getNumberCondition(Operator.EQUALS, numberValues.equal),
          Operator.OR,
          getStringCondition(Operator.EQUALS, stringValues.not_equal),
        ),
      ],
      lie: [
        getCompositeCondition(
          getNumberCondition(Operator.EQUALS, numberValues.lower),
          Operator.OR,
          getStringCondition(Operator.EQUALS, stringValues.not_equal),
        ),
      ],
    },
    nand: {
      truth: [
        getCompositeCondition(
          getNumberCondition(Operator.EQUALS, numberValues.lower),
          Operator.NAND,
          getStringCondition(Operator.EQUALS, stringValues.equal),
        ),
        getCompositeCondition(
          getNumberCondition(Operator.EQUALS, numberValues.equal),
          Operator.NAND,
          getStringCondition(Operator.EQUALS, stringValues.not_equal),
        ),
        getCompositeCondition(
          getNumberCondition(Operator.EQUALS, numberValues.lower),
          Operator.NAND,
          getStringCondition(Operator.EQUALS, stringValues.not_equal),
        ),
      ],
      lie: [
        getCompositeCondition(
          getNumberCondition(Operator.EQUALS, numberValues.equal),
          Operator.NAND,
          getStringCondition(Operator.EQUALS, stringValues.equal),
        ),
      ],
    },
    nor: {
      truth: [
        getCompositeCondition(
          getNumberCondition(Operator.EQUALS, numberValues.lower),
          Operator.NOR,
          getStringCondition(Operator.EQUALS, stringValues.not_equal),
        ),
      ],
      lie: [
        getCompositeCondition(
          getNumberCondition(Operator.EQUALS, numberValues.equal),
          Operator.NOR,
          getStringCondition(Operator.EQUALS, stringValues.equal),
        ),
        getCompositeCondition(
          getNumberCondition(Operator.EQUALS, numberValues.lower),
          Operator.NOR,
          getStringCondition(Operator.EQUALS, stringValues.equal),
        ),
        getCompositeCondition(
          getNumberCondition(Operator.EQUALS, numberValues.equal),
          Operator.NOR,
          getStringCondition(Operator.EQUALS, stringValues.not_equal),
        ),
      ],
    },
    xor: {
      truth: [
        getCompositeCondition(
          getNumberCondition(Operator.EQUALS, numberValues.equal),
          Operator.XOR,
          getStringCondition(Operator.EQUALS, stringValues.not_equal),
        ),
        getCompositeCondition(
          getStringCondition(Operator.EQUALS, stringValues.not_equal),
          Operator.XOR,
          getNumberCondition(Operator.EQUALS, numberValues.equal),
        ),
      ],
      lie: [
        getCompositeCondition(
          getStringCondition(Operator.EQUALS, stringValues.equal),
          Operator.XOR,
          getNumberCondition(Operator.EQUALS, numberValues.equal),
        ),
        getCompositeCondition(
          getStringCondition(Operator.EQUALS, stringValues.not_equal),
          Operator.XOR,
          getNumberCondition(Operator.EQUALS, numberValues.lower),
        ),
        getCompositeCondition(
          getNumberCondition(Operator.EQUALS, numberValues.equal),
          Operator.XOR,
          getStringCondition(Operator.EQUALS, stringValues.equal),
        ),
        getCompositeCondition(
          getNumberCondition(Operator.EQUALS, numberValues.lower),
          Operator.XOR,
          getStringCondition(Operator.EQUALS, stringValues.not_equal),
        ),
      ],
    },
    not: {
      truth: [
        getCompositeCondition(
          getNumberCondition(Operator.EQUALS, numberValues.lower),
          Operator.NOT,
        ),
        getCompositeCondition(
          getStringCondition(Operator.EQUALS, stringValues.not_equal),
          Operator.NOT,
        ),
      ],
      lie: [
        getCompositeCondition(
          getNumberCondition(Operator.EQUALS, numberValues.equal),
          Operator.NOT,
        ),
        getCompositeCondition(
          getStringCondition(Operator.EQUALS, stringValues.equal),
          Operator.NOT,
        ),
      ],
    },
  },
};

/** Creates a deep copy of field definitions and adds visibility condition to a specified field */
const fieldDefinitionWithCondition =
  (field_name: string, condition: Statement, fieldDefinition: FieldDefinitions): FieldDefinitions => {
    const res = _.cloneDeep(fieldDefinition);
    res.fields[field_name].conditionalVisibility = condition;
    return res;
  };

/** Short version of the function for testing purposes, we should mostly set conditions for a certain field */
const addConditionFieldCondition =
  (condition: Statement, fieldDefinition: FieldDefinitions): FieldDefinitions => (
    fieldDefinitionWithCondition('conditionedField', condition, fieldDefinition)
  );

const testCondition =
  (condition: Statement, expectedVisibility: boolean) => {
    const definition = addConditionFieldCondition(condition, fieldDefinitions);
    const payload: FormPayload = FormPayload.create(fieldValues, new FormLayout(definition as DfForm.FormLayoutJSON));

    const visible = calculateVisibility(payload, definition.fields.conditionedField.conditionalVisibility);
    expect(visible).toBe(expectedVisibility);
  };

const testConditions =
  (typeConditions: TypeConditions) => {
    for (const [, pairConditions] of Object.entries(typeConditions)) {
      for (const condition of pairConditions.truth) {
        testCondition(condition, true);
      }
      for (const condition of pairConditions.lie) {
        testCondition(condition, false);
      }
    }
  };

/** Some clean coder would be very proud... if this was all there was in this file.  */
describe('ConditionalVisibilityUtils', () => {
  it('Test Condition Making Function', () => {
    let definition = addConditionFieldCondition(
      getNumberCondition(Operator.EQUALS, fieldValues.numberCondition),
      fieldDefinitions,
    );
    expect(definition.fields.conditionedField.conditionalVisibility).toBeDefined();

    definition = addConditionFieldCondition(null, definition);
    expect(definition.fields.conditionedField.conditionalVisibility).toBeDefined();
    expect(definition.fields.conditionedField.conditionalVisibility).toBeNull();
  });
});

describe('XOR function test', () => {
  it('Test XOR', () => {
    expect(XOR(false, false)).toBe(false);
    expect(XOR(true, false)).toBe(true);
    expect(XOR(false, true)).toBe(true);
    expect(XOR(true, true)).toBe(false);
  });
});

describe('ConditionalVisibility', () => {
  it('Test Number Condition Statement', () => {
    testConditions(conditions.numberConditions);
  });
  it('Test String Condition Statement', () => {
    testConditions(conditions.stringConditions);
  });
  it('Test Null Condition Statement', () => {
    testConditions(conditions.nullConditions);
  });
  it('Test Composite Statements', () => {
    testConditions(conditions.compositeConditions);
  });
  it('Test Unknown Operator', () => {
    expect(() => testCondition(getNumberCondition(-100, 0), false)).toThrow(Error);
    expect(() => testCondition(getNumberCondition(100, 0), false)).toThrow(Error);
  });
});
