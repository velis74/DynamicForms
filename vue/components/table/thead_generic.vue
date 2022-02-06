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
import TableRow from './definitions/row';
import RenderMeasured from './render_measure';
import GenericTRow from './trow_generic';

export default {
  name: 'GenericTHead',
  components: { GenericTRow },
  mixins: [RenderMeasured],
  props: { renderedColumns: { type: Object, required: true } },
  computed: {
    rowData() {
      return new TableRow(this.renderedColumns.items.reduce((result, col) => {
        result[col.name] = col.label;
        return result;
      }, {}));
    },
  },
};
</script>
