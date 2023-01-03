import RowTypesEnum from './row-types';

export default {
  name: 'RowTypes',
  props: {
    rowType: {
      type: Object,
      default: () => RowTypesEnum.Data,
      validator(value: any) {
        return RowTypesEnum.isDefined(value);
      },
    },
  },
  computed: {
    filterRowType() { return RowTypesEnum.Filter; },
    labelRowType() { return RowTypesEnum.Label; },
    dataRowType() { return RowTypesEnum.Data; },
    // @ts-ignore
    thead(): boolean { return RowTypesEnum.headerRows().includes(this.rowType); },
  },
};
