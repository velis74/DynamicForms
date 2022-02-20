import ResizeObserver from 'resize-observer-polyfill';

import TranslationsMixin from '../util/translations_mixin';

import ColumnDisplay from './definitions/display_mode';
import IndexedColumns from './definitions/indexed_columns';
import { ResponsiveLayouts } from './definitions/responsive_layout';
import TableRow from './definitions/row';
import TableRows from './definitions/rows';
import RenderMeasured from './render_measure';
import TableStyle from './table_style';

/**
 * Base Table mixin: provides logic for table component.
 *
 * See table_bootstrap.vue & table_vuetify.vue for respective component declarations
 */
export default {
  mixins: [RenderMeasured, TableStyle, TranslationsMixin],
  props: {
    pkName: { type: String, required: true },
    title: { type: String, required: true },
    columns: { type: Array, required: true },
    columnDefs: { type: Object, required: true },
    rows: { type: TableRows, required: true },
    loading: { type: Boolean, default: false },
  },
  data() { return { containerWidth: null, resizeObserver: null }; },
  computed: {
    renderedColumns() {
      return new IndexedColumns(this.columns.filter(
        (column) => (column.visibility === ColumnDisplay.FULL || column.visibility === ColumnDisplay.INVISIBLE),
      ));
    },
    dataColumns() { return this.columns.filter((column) => column.visibility === ColumnDisplay.HIDDEN); },
    theadRowData() {
      // Creates a fake table row with column labels for data
      return new TableRow(this.renderedColumns.reduce((result, col) => {
        result[col.name] = col.label;
        return result;
      }, {}));
    },
    responsiveLayouts() { return new ResponsiveLayouts(this.renderedColumns); },
    responsiveLayout() { return this.responsiveLayouts.recalculate(this.containerWidth || 0); },
    responsiveLayoutWidth() { return this.responsiveLayout.totalWidth; },
    responsiveColumns() { return this.responsiveLayout.columns; },
  },
  created() {
    this.resizeObserver = new ResizeObserver((entries) => {
      // while redrawing, sometimes ResizeObserver will report width for the old as well as for the new element
      const width = Math.max.apply(null, entries.map((entry) => entry.contentRect.width));
      // while redrawing, ResizeObserver will ofter report the old element being resized to zero
      if (width) this.containerWidth = entries[0].contentRect.width;
    });
  },
  mounted() { this.resizeObserver.observe(this.$refs.container); },
  updated() { this.resizeObserver.observe(this.$refs.container); },
  unmounted() { this.resizeObserver.disconnect(); },
  methods: {
    onMeasure(refName, maxWidth) {
      this.containerWidth = maxWidth;
    },
  },
};
