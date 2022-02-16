import ResizeObserver from 'resize-observer-polyfill';

import TranslationsMixin from '../util/translations_mixin';

import { ResponsiveLayouts } from './definitions/responsive_layout';
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
    responsiveLayouts() { return new ResponsiveLayouts(this.renderedColumns); },
    responsiveColumns() {
      return this.renderedColumns; // this.responsiveLayouts.recalculate(this.containerWidth);
    },
  },
  created() {
    this.resizeObserver = new ResizeObserver((entries) => {
      this.containerWidth = entries[0].contentRect.width;
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
