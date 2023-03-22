<template>
  <div>
    <div v-for="(row, row_index) in column.rows" :key="row_index" class="sub-row">
      <GenericColumn
        v-for="field in row.fields"
        :key="field.name"
        :column="field"
        :row-data="rowData"
        :row-type="rowType"
        :thead="thead"
        :actions="actions"
      />
    </div>
  </div>
</template>

<script lang="ts">
import { defineComponent } from 'vue';

import FilteredActions from '../actions/filtered-actions';

import TableColumn from './definitions/column';
import RowTypesMixin from './row-types-mixin';

export default /* #__PURE__ */ defineComponent({
  name: 'ColumnGroup',
  mixins: [RowTypesMixin],
  props: {
    column: { type: TableColumn, required: true },
    rowData: { type: Object, required: true },
    actions: { type: FilteredActions, required: true },
  },
});
</script>
