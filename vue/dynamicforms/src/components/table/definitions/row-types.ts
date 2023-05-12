enum RowTypes {
  Label = 0,
  Filter = 1,
  Data = 2,
}

namespace RowTypes {
  export function headerRows() { return [RowTypes.Label, RowTypes.Filter]; }

  export function isDefined(rowType: number) {
    return Object.values(RowTypes).includes(rowType);
  }

  export function isTHead(rowType: RowTypes) { return [RowTypes.Label, RowTypes.Filter].includes(rowType); }
}

Object.freeze(RowTypes);
export default RowTypes;
