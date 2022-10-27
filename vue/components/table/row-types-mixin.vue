<script>
import RowTypesEnum from './row-types-enum';

export default {
  name: 'RowTypes',
  props: { rowType: { type: Number, default: RowTypesEnum.Data } },
  computed: {
    filterRowType() { return RowTypesEnum.Filter; },
    labelRowType() { return RowTypesEnum.Label; },
    dataRowType() { return RowTypesEnum.Data; },
    thead() { return [RowTypesEnum.Label, RowTypesEnum.Filter].includes(this.rowType); },
  },
};
</script>
