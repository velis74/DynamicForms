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

<script>
import FilteredActions from '../actions/filtered-actions';

import TableColumn from './definitions/column';
import RenderMeasured from './render-measure';
import RowTypesMixin from './row-types-mixin';

export default {
  name: 'ColumnGroup',
  mixins: [RenderMeasured, RowTypesMixin],
  props: {
    thead: { type: Boolean, default: false }, // is this row rendered in thead section
    column: { type: TableColumn, required: true },
    rowData: { type: Object, required: true },
    actions: { type: FilteredActions, default: null },
  },
  methods: {
    onMeasure(refName, maxWidth) {
      if (refName === 'column') {
        this.column.setMaxWidth(maxWidth);
      }
    },
  },
};
</script>
