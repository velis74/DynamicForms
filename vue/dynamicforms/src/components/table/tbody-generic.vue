<template>
  <div ref="tbodyElement" class="df-tbody">
    <!--
     IntersectionObserver currently not used. See rows-visibility-observer.ts
     v-observe-visibility="rows.visibilityHandler(row[pkName])"
     -->
    <GenericTRow
      v-for="row in rows.data"
      :key="row[pkName]"
      :rendered-columns="renderedColumns"
      :row-data="row"
      :row-type="RowTypes.Data"
      :actions="actions"
    />
  </div>
</template>
<script setup lang="ts">
import { computed, ref } from 'vue';

import FilteredActions from '../actions/filtered-actions';
import IndexedArray from '../classes/indexed-array';

import TableColumn from './definitions/column';
import RowTypes from './definitions/row-types';
import TableRows from './definitions/rows';
import useRowVisibilityObserver from './rows-visibility-observer.js';
import GenericTRow from './trow-generic.vue';

const props = defineProps<{
  pkName: string
  renderedColumns: IndexedArray<TableColumn>
  rows: TableRows
  actions: FilteredActions
}>();
const tbodyElement = ref();
useRowVisibilityObserver(tbodyElement, computed(() => props.rows));
</script>
