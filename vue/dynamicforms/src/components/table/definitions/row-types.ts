enum RowTypes {
  Label = 0,
  Filter = 1,
  Data = 2,
}

namespace RowTypes {
  export const headerRows: RowTypes[] = [RowTypes.Label, RowTypes.Filter];

  export function isDefined(rowType: number): boolean {
    return Object.values(RowTypes).includes(rowType);
  }

  export function isTHead(rowType: RowTypes): boolean { return RowTypes.headerRows.includes(rowType); }
}

Object.freeze(RowTypes);
export default RowTypes;
