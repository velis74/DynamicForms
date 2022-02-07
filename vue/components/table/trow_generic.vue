<template>
  <div ref="row" :class="`df-row ${rowData.dfControlStructure.CSSClass}`" :style="rowData.dfControlStructure.CSSStyle">
    <div
      v-for="column in renderedColumns.items"
      :key="column.name"
      :ref="`col-${column.name}`"
      :class="`df-col text-${column.align} ${customClass(column)}`"
      @click.stop="(event) => orderClick(column.name, event)"
    >
      {{ rowData[column.name] }}
      <OrderingIndicator v-if="thead" :ref="`ordering-${column.name}`" :ordering="column.ordering"/>
    </div>
  </div>
</template>

<script>
import OrderingIndicator from './ordering_indicator';
import RenderMeasured from './render_measure';

export default {
  name: 'GenericTRow',
  components: { OrderingIndicator },
  mixins: [RenderMeasured],
  props: {
    renderedColumns: { type: Object, required: true },
    dataColumns: { type: Array, required: true },
    rowData: { type: Object, required: true },
    thead: { type: Boolean, default: false }, // is this row rendered in thead section
  },
  methods: {
    customClass(column) {
      let res = this.rowData.dfControlStructure.CSSClass;
      if (this.thead) res = `${res} ${this.rowData.dfControlStructure.CSSClassHead}`.trim();
      if (column.ordering.isOrderable) res = `${res} ordering`.trim();
      return res;
    },
    orderClick(colName, event) {
      this.$refs[`ordering-${colName}`][0].orderClick(event); // defer handling the click to ordering indicator
    },
  },
};
</script>
