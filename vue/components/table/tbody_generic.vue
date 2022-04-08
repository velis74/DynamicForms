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
<script>
import { ObserveVisibility } from 'vue-observe-visibility';

import FilteredActions from '../actions/filtered_actions';
import IndexedArray from '../classes/indexed_array';

import TableRows from './definitions/rows';
import RowsVisibilityObserver from './rows_visibility_observer';
import GenericTRow from './trow_generic';

export default {
  name: 'GenericTBody',
  directives: { 'observe-visibility': ObserveVisibility },
  components: { GenericTRow },
  mixins: [RowsVisibilityObserver],
  props: {
    pkName: { type: String, required: true },
    renderedColumns: { type: IndexedArray, required: true },
    dataColumns: { type: Array, required: true },
    rows: { type: TableRows, required: true },
    actions: { type: FilteredActions, default: null },
  },
};
</script>
