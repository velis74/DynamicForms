<template>
  <div
    ref="row"
    :class="`df-row ${rowData.dfControlStructure.CSSClass}`"
    :style="rowData.dfControlStructure.CSSStyle"
    @click.stop="(event) => rowClick(event, 'ROW_CLICK', null)"
    @mouseup.right="rowClick($event,'ROW_RIGHTCLICK', row)"
  >
    <div
      v-for="column in renderedColumns.items"
      :key="column.name"
      :ref="`col-${column.name}`"
      :class="`df-col text-${column.align} ${customClass(column)}`"
      @click.stop="(event) => rowClick(event, 'ROW_CLICK', column)"
      @mouseup.right="rowClick($event,'ROW_RIGHTCLICK', column)"
    >
      <!-- first we render any field start actions -->
      <!--Actions :thead="thead" :row-data="rowData" :actions="actions.filter('FIELD_START', column.name)"/-->
      <!-- then the field component itself -->
      <component
        :is="column.renderComponentName"
        v-if="column.renderComponentName"
        :row-data="rowData"
        :column="column"
        :thead="thead"
      />
      <!-- but maybe the field component is actually a row start / end actions field -->
      <!--Actions
        v-else-if="['#actions-row_start', '#actions-row_end'].includes(column.name)"
        :thead="thead"
        :row-data="rowData"
        :actions="actions.filter(column.name.substr(9).toUpperCase())"
      /-->
      <!-- or it's just a decorated text and not a component -->
      <div v-else v-html="column.renderDecoratorFunction(rowData, thead)"/>
      <!-- we finish up with any field end actions -->
      <!--Actions :thead="thead" :row-data="rowData" :actions="actions.filter('FIELD_END', column.name)"/-->
      <OrderingIndicator v-if="thead" :ref="`ordering-${column.name}`" :ordering="column.ordering"/>
    </div>
  </div>
</template>

<script>
import * as TableCells from './cell-renderers';
import OrderingIndicator from './ordering_indicator';
import RenderMeasured from './render_measure';

export default {
  name: 'GenericTRow',
  components: { OrderingIndicator, ...TableCells },
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
    rowClick(event, eventsFilter, column) {
      if (this.thead && eventsFilter === 'ROW_CLICK' && column) {
        // A column in thead was clicked: adjust sorting
        this.$refs[`ordering-${column.name}`][0].orderClick(event); // defer handling the click to ordering indicator
      }
    },
  },
};
</script>
