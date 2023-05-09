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
    @click.stop="(event) => dispatchAction(this, actions.rowClick, { rowType, event })"
    @mouseup.right="(event) => dispatchAction(this, actions.rowRightClick, { rowType, event })"
  >
    <GenericColumn
      v-for="column in renderedColumns.items"
      :key="column.name"
      :column="column as TableColumn"
      :row-data="payload"
      :actions="actions"
      :filter-row="filterDefinition ? filterDefinition.columns[column.name] || new TableColumn({}, []) : null"
    />
  </div>
</template>

<script setup lang="ts">
import { computed, defineComponent, provide, ref } from 'vue';
import { ObserveVisibility } from 'vue-observe-visibility';

import { dispatchAction } from '../actions/action-handler-mixin';
import FilteredActions from '../actions/filtered-actions';
import IndexedArray from '../classes/indexed-array';

import TableColumn from './definitions/column';
import TableFilterRow from './definitions/filterrow';
import TableRow from './definitions/row';
import { useRenderMeasure } from './render-measure';
import RowTypesEnum from './row-types-enum';

const props = withDefaults(
  defineProps<{
    renderedColumns: IndexedArray<TableColumn>,
    // dataColumns: Array,
    rowData: TableRow,
    actions: FilteredActions,
    filterDefinition?: TableFilterRow,
    rowType: RowTypesEnum,
  }>(),
  { filterDefinition: undefined },
);

if (props.rowType && !RowTypesEnum.isDefined(props.rowType)) {
  console.warn(`Prop row-type of trow-generic set to a wrong value (${props.rowType})`);
}
provide('row-type', props.rowType);

const thead = computed(() => RowTypesEnum.isTHead(props.rowType));
const rowInfiniteStyle = computed(() => (
  `${props.rowData.dfControlStructure.CSSStyle};` +
  `width: 1px; height: ${props.rowData.dfControlStructure.measuredHeight || 10}px`
));
const payload = computed(() => (props.filterDefinition ? props.filterDefinition.payload : props.rowData));

function onMeasure(refName: string, maxWidth: number, maxHeight: number) {
  if (props.rowData.dfControlStructure.isShowing) {
    props.rowData.setMeasuredHeight(maxHeight);
  }
}

const row = ref();
useRenderMeasure(onMeasure, { row });
</script>
<script lang="ts">
export default defineComponent({
  name: 'GenericTRow',
  directives: { 'observe-visibility': ObserveVisibility },
});
</script>
