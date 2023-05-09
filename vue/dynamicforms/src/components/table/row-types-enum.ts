enum RowTypesEnum {
  Label = 0,
  Filter = 1,
  Data = 2,
}

namespace RowTypesEnum {
  export function headerRows() { return [RowTypesEnum.Label, RowTypesEnum.Filter]; }

  export function isDefined(rowType: number) {
    return Object.values(RowTypesEnum).includes(rowType);
  }

  export function isTHead(rowType: RowTypesEnum) { return [RowTypesEnum.Label, RowTypesEnum.Filter].includes(rowType); }
}

Object.freeze(RowTypesEnum);
export default RowTypesEnum;
