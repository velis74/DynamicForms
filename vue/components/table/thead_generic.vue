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
  props: {
    renderedColumns: { type: IndexedColumns, required: true },
    rowData: { type: TableRow, required: true },
  },
  methods: {
    onMeasure(refName, maxWidth, maxHeight) {
      this.rowData.setMeasuredHeight(maxHeight);
    },
  },
};
</script>
