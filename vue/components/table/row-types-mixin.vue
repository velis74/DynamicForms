<script>
import RowTypes from './row-types';

export default {
  name: 'RowTypes',
  props: { rowType: { type: Number, default: RowTypes.Data } },
  computed: {
    filterType() { return RowTypes.Filter; },
    labelType() { return RowTypes.Label; },
    dataType() { return RowTypes.Data; },
    headerTypes() { return [RowTypes.Label, RowTypes.Filter]; },
    thead() { return this.headerTypes.includes(this.rowType); },
  },
};
</script>
