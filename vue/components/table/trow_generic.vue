<template>
  <div
    v-if="!rowData.dfControlStructure.isShowing && !thead"
    :class="`df-row ${rowData.dfControlStructure.CSSClass}`"
    :style="rowInfiniteStyle"
  />
  <div
    v-else
    ref="row"
    :class="`df-row ${rowData.dfControlStructure.CSSClass}`"
    :style="rowData.dfControlStructure.CSSStyle"
    @click.stop="(event) => rowClick(event, 'ROW_CLICK', null)"
    @mouseup.right="rowClick($event,'ROW_RIGHTCLICK', null)"
  >
    <GenericColumn
      v-for="column in renderedColumns.items"
      :key="column.name"
      :column="column"
      :row-data="rowData"
      :thead="thead"
    />
  </div>
</template>

<script>
import { ObserveVisibility } from 'vue-observe-visibility';

import IndexedColumns from './definitions/indexed_columns';
import RenderMeasured from './render_measure';

export default {
  name: 'GenericTRow',
  directives: { 'observe-visibility': ObserveVisibility },
  mixins: [RenderMeasured],
  props: {
    renderedColumns: { type: IndexedColumns, required: true },
    dataColumns: { type: Array, required: true },
    rowData: { type: Object, required: true },
    thead: { type: Boolean, default: false }, // is this row rendered in thead section
  },
  // beforeMount() { console.log('beforeMount', this.rowData.id); },
  // beforeUpdate() { console.log('beforeUpdate', this.rowData.id); },
  computed: {
    rowInfiniteStyle() {
      // For rows not currently rendered, we set a fixed width & height. Height is 10 if it hadn't been computed yet
      return (
        `${this.rowData.dfControlStructure.CSSStyle};` +
        `width: 1px; height: ${this.rowData.dfControlStructure.measuredHeight || 10}px`
      );
    },
  },
  methods: {
    onMeasure(refName, maxWidth, maxHeight) {
      if (this.rowData.dfControlStructure.isShowing) {
        this.rowData.setMeasuredHeight(maxHeight);
      }
    },
    // eslint-disable-next-line no-unused-vars
    rowClick(event, eventsFilter, column) {
      // we're currently not processing any clicks outside column cells
    },
  },
};
</script>
