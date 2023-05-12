<template>
  <div ref="dfthead" class="df-thead">
    <GenericTRow
      :rendered-columns="renderedColumns"
      :data-columns="[]"
      :row-data="rowData"
      :actions="actions"
      :row-type="RowTypes.Label"
    />
    <GenericTRow
      v-if="filterDefinition"
      :rendered-columns="renderedColumns"
      :data-columns="[]"
      :row-data="rowData"
      :actions="actions"
      :filter-definition="filterDefinition"
      :row-type="RowTypes.Filter"
    />
    <div class="df-separator"/>
  </div>
</template>
<script setup lang="ts">
import { defineComponent, ref } from 'vue';

import FilteredActions from '../actions/filtered-actions';
import IndexedArray from '../classes/indexed-array';

import TableColumn from './definitions/column';
import TableFilterRow from './definitions/filterrow';
import TableRow from './definitions/row';
import { useRenderMeasure } from './render-measure';
import RowTypes from './definitions/row-types';
import GenericTRow from './trow-generic.vue';

const props = withDefaults(
  defineProps<{ // Can't just import the interface - vue complains. https://github.com/vuejs/core/issues/4294
    renderedColumns: IndexedArray<TableColumn>,
    rowData: TableRow,
    actions: FilteredActions,
    filterDefinition?: TableFilterRow;
  }>(),
  { filterDefinition: undefined },
);

const dfthead = ref();

function onMeasure(refName: string, maxWidth: number, maxHeight: number) {
  props.rowData.setMeasuredHeight(maxHeight);
}
useRenderMeasure(onMeasure, { dfthead });
</script>
<script lang="ts">
export default defineComponent({ name: 'GenericTHead' });
</script>
