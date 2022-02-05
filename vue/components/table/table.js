import TableRows from '../api_consumer/table_rows';
import ColumnDisplay from '../util/display_mode';

import TableColumnSizer from './table_column_sizer';

/**
 * Base Table mixin: provides logic for table component.
 *
 * See table_bootstrap.vue & table_vuetify.vue for respective component declarations
 */
export default {
  mixins: [TableColumnSizer],
  props: {
    pkName: { type: String, required: true },
    title: { type: String, required: true },
    columns: { type: Array, required: true },
    columnDefs: { type: Object, required: true },
    rows: { type: TableRows, required: true },
    wrap: { type: Boolean, default: false },
  },
  data() { return {}; },
  computed: {
    renderedColumns() {
      return this.columns.filter(
        (column) => (column.visibility === ColumnDisplay.FULL || column.visibility === ColumnDisplay.INVISIBLE),
      );
    },
    dataColumns() { return this.columns.filter((column) => column.visibility === ColumnDisplay.HIDDEN); },
  },
};
