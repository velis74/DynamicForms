<template>
  <div ref="tbodyElement" class="df-tbody">
    <!--
     IntersectionObserver currently not used. See rows-visibility-observer.ts
     v-observe-visibility="rows.visibilityHandler(row[pkName])"
     -->
    <GenericTRow
      :is="row.dfControlStructure.componentName"
      v-for="row in rows.data"
      :key="row[pkName]"
      :rendered-columns="renderedColumns"
      :data-columns="dataColumns"
      :row-data="row"
      :row-type="RowTypesEnum.Data"
      :actions="actions"
    />
  </div>
</template>
<script setup lang="ts">
import { ref, toRefs } from 'vue';
// import { ObserveVisibility as vObserveVisibility } from 'vue-observe-visibility';

import FilteredActions from '../actions/filtered-actions';
import IndexedArray from '../classes/indexed-array';

import TableColumn from './definitions/column';
import TableRows from './definitions/rows';
import RowTypesEnum from './row-types-enum';
import useRowVisibilityObserver from './rows-visibility-observer.js';
import GenericTRow from './trow-generic.vue';

// export default defineComponent({
//   name: 'GenericTBody',
//   directives: { 'observe-visibility': ObserveVisibility },
//   mixins: [RowsVisibilityObserver],
const props = defineProps<{
  pkName: string
  renderedColumns: IndexedArray<TableColumn>
  dataColumns: TableColumn[]
  rows: TableRows
  actions: FilteredActions
}>();
const tbodyElement = ref();
useRowVisibilityObserver(tbodyElement, props.rows);
const { pkName, renderedColumns, dataColumns, rows, actions } = toRefs(props);
</script>
