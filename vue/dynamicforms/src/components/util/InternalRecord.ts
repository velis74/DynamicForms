import _ from 'lodash';

type Internal<T extends object> = T & {
  readonly ['__pk_name']: keyof T;
};

export default function createInternalRecord <T extends object>(
  record: T,
  pkName: keyof T & string,
  pkValue?: any,
): Internal<T> {
  return new Proxy(record, {
    get: (target: T, property: keyof T & (string | symbol)) => {
      if (property === pkName) {
        return target[property] ?? pkValue;
      }
      if (property === '__pk_name') return pkName;

      return target[property];
    },
    set: (target: T, property: keyof T & (string | symbol), value: any) => {
      if (property !== pkName) target[property] = value;
      return true;
    },
  }) as Internal<T>;
}

export function toExternalRecordCopy<T extends object>(record: Internal<T>): T {
  const el = _.cloneDeep(record);
  // eslint-disable-next-line no-underscore-dangle
  const pkName = record.__pk_name;

  el[pkName] = record[pkName];
  return el;
}
