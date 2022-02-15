<template>
  <div
    ref="row"
    :class="`df-row ${rowData.dfControlStructure.CSSClass}`"
    :style="rowData.dfControlStructure.CSSStyle"
    @click.stop="(event) => rowClick(event, 'ROW_CLICK', null)"
    @mouseup.right="rowClick($event,'ROW_RIGHTCLICK', null)"
  >
    <GenericColumn
      v-for="column in renderedColumns.items"
      :key="column.name"
      :column="column"
      :row-data="rowData"
      :thead="thead"
    />
  </div>
</template>

<script>
import RenderMeasured from './render_measure';
import GenericColumn from './tcolumn_generic';

export default {
  name: 'GenericTRow',
  components: { GenericColumn },
  mixins: [RenderMeasured],
  props: {
    renderedColumns: { type: Object, required: true },
    dataColumns: { type: Array, required: true },
    rowData: { type: Object, required: true },
    thead: { type: Boolean, default: false }, // is this row rendered in thead section
  },
  methods: {
    onMeasure(refName, maxWidth, maxHeight) {
      this.rowData.setMeasuredHeight(maxHeight);
    },
    // eslint-disable-next-line no-unused-vars
    rowClick(event, eventsFilter, column) {
      // we're currently not processing any clicks outside column cells
    },
  },
};
</script>
