<template>
  <div ref="df-thead" class="df-thead">
    <div
      ref="filter-row"
      :class="`df-row ${rowData.dfControlStructure.CSSClass}`"
      :style="rowData.dfControlStructure.CSSStyle"
    >
      <div v-for="(column, idx) in renderedColumns.items" :key="idx">
        {{ pri(column) }}
      </div>

      <FormField
        :is="column.layoutFieldComponentName"
        v-for="(column, idx) in renderedColumns.items"
        :key="`${idx}${column.renderKey}`"
        :field="column"
        :payload="rowData"
        :errors="errors"
      />
    </div>
  </div>
</template>
<script>
import FilteredActions from '../actions/filtered_actions';
import IndexedArray from '../classes/indexed_array';
import FormField from '../form/field';

import TableRow from './definitions/row';
import RenderMeasured from './render_measure';

export default {
  name: 'GenericTFilterRow',
  components: { FormField },
  mixins: [RenderMeasured],
  props: {
    renderedColumns: { type: IndexedArray, required: true },
    rowData: { type: TableRow, required: true },
    actions: { type: FilteredActions, default: null },
  },
  data() {
    return { errors: {} };
  },
  methods: {
    pri(t) {
      console.log(t);
    },
  },
};
</script>
