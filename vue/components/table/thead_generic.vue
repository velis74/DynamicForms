<template>
  <div ref="df-thead" class="df-thead">
    <GenericTRow
      :rendered-columns="renderedColumns"
      :data-columns="[]"
      :row-data="rowData"
      thead
    />
    <div class="df-separator"/>
  </div>
</template>
<script>
import IndexedColumns from './definitions/indexed_columns';
import TableRow from './definitions/row';
import RenderMeasured from './render_measure';
import GenericTRow from './trow_generic';

export default {
  name: 'GenericTHead',
  components: { GenericTRow },
  mixins: [RenderMeasured],
  props: { renderedColumns: { type: IndexedColumns, required: true } },
  computed: {
    rowData() {
      // Creates a fake table row with column labels for data
      return new TableRow(this.renderedColumns.reduce((result, col) => {
        result[col.name] = col.label;
        return result;
      }, {}));
    },
  },
  methods: {
    onMeasure(refName, maxWidth, maxHeight) {
      this.rowData.dfControlStructure.measuredHeight = maxHeight;
    },
  },
};
</script>
