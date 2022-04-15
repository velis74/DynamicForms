<template>
  <div
    ref="column"
    :class="`${columnClass} ${column.name} text-${column.align} ${customClass(column)}`"
    @click.stop="(event) => rowClick(event, 'ROW_CLICK', column)"
    @mouseup.right="rowClick($event,'ROW_RIGHTCLICK', column)"
  >
    <!-- first we render any field start actions -->
    <!--Actions :thead="thead" :row-data="rowData" :actions="actions.filter('FIELD_START', column.name)"/-->
    <!-- then the field component itself -->
    <component
      :is="actionsComponentName"
      v-if="!thead"
      :actions="actions.fieldStart(column.name)"
    />
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
    <OrderingIndicator v-if="thead" ref="ordering" :ordering="column.ordering"/>
    <component
      :is="actionsComponentName"
      v-if="!thead"
      :actions="actions.fieldEnd(column.name)"
    />
    <component
      :is="actionsComponentName"
      v-if="!thead && column.name === '#actions-row_end'"
      :actions="actions.rowEnd()"
    />
  </div>
</template>

<script>
import ActionsUtil from '../actions/actions_util';
import FilteredActions from '../actions/filtered_actions';

import * as TableCells from './cell-renderers';
import ColumnGroup from './column_group';
import TableColumn from './definitions/column';
import OrderingIndicator from './ordering_indicator';
import RenderMeasured from './render_measure';

export default {
  name: 'GenericColumn',
  components: { ColumnGroup, OrderingIndicator, ...TableCells },
  mixins: [RenderMeasured, ActionsUtil],
  props: {
    thead: { type: Boolean, default: false }, // is this row rendered in thead section
    column: { type: TableColumn, required: true },
    rowData: { type: Object, required: true },
    actions: { type: FilteredActions, default: null },
  },
  computed: { columnClass() { return this.column.renderComponentName === 'ColumnGroup' ? 'column-group' : 'df-col'; } },
  methods: {
    onMeasure(refName, maxWidth) {
      if (refName === 'column') {
        this.column.setMaxWidth(maxWidth);
      }
    },
    customClass(column) {
      let res = column.CSSClass;
      if (this.thead) res = `${res} ${column.CSSClassHead}`.trim();
      return res;
    },
    rowClick(event, eventsFilter, column) {
      if (this.thead && eventsFilter === 'ROW_CLICK' && column) {
        // A column in thead was clicked: adjust sorting
        this.$refs.ordering.orderClick(event); // defer handling the click to ordering indicator
      }
    },
  },
};
</script>
