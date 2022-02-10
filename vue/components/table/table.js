import TranslationsMixin from '../util/translations_mixin';

import TableRows from './definitions/rows';
import TableColumnSizer from './table_style';

/**
 * Base Table mixin: provides logic for table component.
 *
 * See table_bootstrap.vue & table_vuetify.vue for respective component declarations
 */
export default {
  mixins: [TableColumnSizer, TranslationsMixin],
  props: {
    pkName: { type: String, required: true },
    title: { type: String, required: true },
    columns: { type: Array, required: true },
    columnDefs: { type: Object, required: true },
    rows: { type: TableRows, required: true },
    wrap: { type: Boolean, default: false },
    loading: { type: Boolean, default: false },
  },
  data() { return {}; },
};
