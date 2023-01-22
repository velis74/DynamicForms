<template>
  <div class="df-tbody">
    <GenericTRow
      :is="row.dfControlStructure.componentName"
      v-for="row in rows.data"
      :key="row[pkName]"
      v-observe-visibility="rows.visibilityHandler(row[pkName])"
      :rendered-columns="renderedColumns"
      :data-columns="dataColumns"
      :row-data="row"
      :actions="actions"
    />
  </div>
</template>
<script lang="ts">
import { defineComponent } from 'vue';
import { ObserveVisibility } from 'vue-observe-visibility';

import FilteredActions from '../actions/filtered-actions';
import IndexedArray from '../classes/indexed-array';

import TableRows from './definitions/rows';
import RowsVisibilityObserver from './rows-visibility-observer';
import GenericTRow from './trow-generic.vue';

export default /* #__PURE__ */ defineComponent({
  name: 'GenericTBody',
  directives: { 'observe-visibility': ObserveVisibility },
  components: { GenericTRow },
  mixins: [RowsVisibilityObserver],
  props: {
    pkName: { type: String, required: true },
    renderedColumns: { type: IndexedArray, required: true },
    dataColumns: { type: Array, required: true },
    rows: { type: TableRows, required: true },
    actions: { type: FilteredActions, required: true },
  },
});
</script>
