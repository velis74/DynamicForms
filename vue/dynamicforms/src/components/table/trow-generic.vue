<template>
  <div
    v-if="!rowData.dfControlStructure.isShowing && !thead"
    :class="`df-row ${rowData.dfControlStructure.CSSClass}`"
    :style="rowInfiniteStyle"
  />
  <div
    v-else
    ref="row"
    :class="{ [`df-row ${rowData.dfControlStructure.CSSClass}`]: true, ['data-row']: rowType === RowTypes.Data }"
    :style="rowData.dfControlStructure.CSSStyle"
    @click.stop="(event) => callHandler(actions.rowClick, { rowType, event })"
    @mouseup.right="(event) => callHandler(actions.rowRightClick, { rowType, event })"
  >
    <GenericColumn
      v-for="column in renderedColumns.items"
      :key="column.name"
      :column="column as TableColumn"
      :row-data="payload"
      :actions="actions"
      :filter-row="filterRow(column)"
      :filter-definition="filterDefinition"
    />
  </div>
</template>

<script setup lang="ts">
import { computed, provide, ref } from 'vue';

import { useActionHandler } from '../actions/action-handler-composable';
import FilteredActions from '../actions/filtered-actions';
import IndexedArray from '../classes/indexed-array';

import TableColumn from './definitions/column';
import TableFilterRow from './definitions/filterrow';
import TableRow from './definitions/row';
import RowTypes from './definitions/row-types';
import { DfTable } from './namespace';
import { useRenderMeasure } from './render-measure';

const props = withDefaults(
  defineProps<{
    renderedColumns: IndexedArray<TableColumn>,
    rowData: TableRow,
    actions: FilteredActions,
    filterDefinition?: TableFilterRow,
    rowType: RowTypes,
  }>(),
  { filterDefinition: undefined },
);

if (props.rowType && !RowTypes.isDefined(props.rowType)) {
  console.warn(`Prop row-type of trow-generic set to a wrong value (${props.rowType})`);
}
provide('row-type', props.rowType);

const thead = computed(() => RowTypes.isTHead(props.rowType));
const rowInfiniteStyle = computed(() => (
  `${props.rowData.dfControlStructure.CSSStyle};` +
  `width: 1px; height: ${props.rowData.dfControlStructure.measuredHeight || 10}px`
));
const payload = computed(() => (props.filterDefinition ? props.filterDefinition.payload : props.rowData));
function filterRow(column: TableColumn) {
  return props.filterDefinition ?
    props.filterDefinition.columns[column.name] || new TableColumn({} as DfTable.ColumnJSON, []) :
    null;
}

provide('payload', payload);

const { callHandler } = useActionHandler();

function onMeasure(refName: string, maxWidth: number, maxHeight: number) {
  if (props.rowData.dfControlStructure.isShowing) {
    props.rowData.setMeasuredHeight(maxHeight);
  }
}

const row = ref();
useRenderMeasure(onMeasure, { row });
</script>
