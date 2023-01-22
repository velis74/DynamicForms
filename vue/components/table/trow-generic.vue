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
    @click.stop="(event) => dispatchAction(actions.rowClick, { rowType, event })"
    @mouseup.right="(event) => dispatchAction(actions.rowRightClick, { rowType, event })"
  >
    <GenericColumn
      v-for="column in renderedColumns.items"
      :key="column.name"
      :column="column"
      :row-data="filterDefinition ? filterDefinition.payload : rowData"
      :row-type="rowType"
      :actions="actions"
      :filter-row="filterDefinition ? filterDefinition.columns[column.name] || new TableColumn({}, []) : null"
    />
  </div>
</template>

<script lang="ts">
import { defineComponent } from 'vue';
import { ObserveVisibility } from 'vue-observe-visibility';

import ActionHandlerMixin from '../actions/action-handler-mixin.vue';
import FilteredActions from '../actions/filtered-actions';
import IndexedArray from '../classes/indexed-array';

import TableColumn from './definitions/column';
import TableFilterRow from './definitions/filterrow';
import RenderMeasured from './render-measure';
import RowTypesMixin from './row-types-mixin';

export default /* #__PURE__ */ defineComponent({
  name: 'GenericTRow',
  directives: { 'observe-visibility': ObserveVisibility },
  mixins: [RenderMeasured, ActionHandlerMixin, RowTypesMixin],
  props: {
    renderedColumns: { type: IndexedArray, required: true },
    dataColumns: { type: Array, required: true },
    rowData: { type: Object, required: true },
    actions: { type: FilteredActions, required: true },
    filterDefinition: { type: TableFilterRow, default: null },
  },
  computed: {
    TableColumn() { return TableColumn; },
    rowInfiniteStyle() {
      // For rows not currently rendered, we set a fixed width & height. Height is 10 if it hadn't been computed yet
      return (
        `${this.rowData.dfControlStructure.CSSStyle};` +
        `width: 1px; height: ${this.rowData.dfControlStructure.measuredHeight || 10}px`
      );
    },
    payload() {
      return this.filterDefinition ? this.filterDefinition.payload : this.rowData;
    },
  },
  methods: {
    onMeasure(refName, maxWidth, maxHeight) {
      if (this.rowData.dfControlStructure.isShowing) {
        this.rowData.setMeasuredHeight(maxHeight);
      }
    },
  },
});
</script>
