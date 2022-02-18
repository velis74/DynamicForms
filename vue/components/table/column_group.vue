<template>
  <div class="column-group">
    <div v-for="(row, row_index) in column.rows" :key="row_index" class="sub-row">
      <GenericColumn
        v-for="field in row.fields"
        :key="field.name"
        :column="field"
        :row-data="rowData"
        :thead="thead"
      />
    </div>
  </div>
</template>

<script>
import TableColumn from './definitions/column';
import RenderMeasured from './render_measure';

export default {
  name: 'ColumnGroup',
  components: { GenericColumn: () => import('./tcolumn_generic') },
  mixins: [RenderMeasured],
  props: {
    thead: { type: Boolean, default: false }, // is this row rendered in thead section
    column: { type: TableColumn, required: true },
    rowData: { type: Object, required: true },
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
