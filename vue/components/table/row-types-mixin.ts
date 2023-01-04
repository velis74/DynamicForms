import { defineComponent } from 'vue';

import RowTypesEnum from './row-types-enum';

export default /* #__PURE__ */ defineComponent({
  name: 'RowTypes',
  props: {
    rowType: {
      type: Object,
      default: () => RowTypesEnum.Data,
      validator(value) {
        return RowTypesEnum.isDefined(value);
      },
    },
  },
  computed: {
    filterRowType() { return RowTypesEnum.Filter; },
    labelRowType() { return RowTypesEnum.Label; },
    dataRowType() { return RowTypesEnum.Data; },
    thead() { return [RowTypesEnum.Label, RowTypesEnum.Filter].includes(this.rowType); },
  },
});
