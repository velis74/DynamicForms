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
      :actions="actions"
      :filter-row="(filterDefinition || {columns: {}}).columns[column.name]"
    />
  </div>
</template>

<script>
import { ObserveVisibility } from 'vue-observe-visibility';

import FilteredActions from '../actions/filtered_actions';
import IndexedArray from '../classes/indexed_array';

import TableFilterRow from './definitions/filterrow';
import RenderMeasured from './render_measure';

export default {
  name: 'GenericTRow',
  directives: { 'observe-visibility': ObserveVisibility },
  mixins: [RenderMeasured],
  props: {
    renderedColumns: { type: IndexedArray, required: true },
    dataColumns: { type: Array, required: true },
    rowData: { type: Object, required: true },
    thead: { type: Boolean, default: false }, // is this row rendered in thead section
    actions: { type: FilteredActions, default: null },
    filterDefinition: { type: TableFilterRow, default: null },
  },
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
      console.log(event, eventsFilter, column);
      if (this.filterDefinition) {
        // eslint-disable-next-line no-useless-return
        return;
      }
      // we're currently not processing any clicks outside column cells
    },
  },
};
</script>
