// @ts-ignore
import Enum from 'enum';

const RowTypesEnum = new Enum({
  Label: 0,
  Filter: 1,
  Data: 2,
}, { freeze: false });

RowTypesEnum.headerRows = () => [RowTypesEnum.Label, RowTypesEnum.Filter];

export default Object.freeze(RowTypesEnum);
