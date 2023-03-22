<template>
  <div
    ref="column"
    :class="`${columnClass} ${column.name} text-${column.align} ${customClass()}`"
    @click.stop="(event) => dispatchAction(actions.rowClick, { column, event, rowType })"
    @mouseup.right="(event) => dispatchAction(actions.rowRightClick, { column, event, rowType })"
  >
    <template v-if="filterRow">
      <FormField
        v-if="filterRow.formFieldInstance"
        :field="filterRow.formFieldInstance"
        :actions="actions"
        :errors="{}"
        style="padding: 0; margin: 0;"
      />
    </template>
    <template v-else>
      <df-actions
        v-if="!thead && column.name === '#actions-row_start' && actions.rowStart.length"
        :actions="actions.rowStart"
        class="actions"
      />
      <!-- first we render any field start actions -->
      <!--Actions :thead="thead" :row-data="rowData" :actions="actions.filter('FIELD_START', column.name)"/-->
      <!-- then the field component itself -->
      <df-actions
        v-if="!thead && actions.fieldStart(column.name).length"
        :actions="actions.fieldStart(column.name)"
        class="actions"
      />
      <div v-if="column.renderComponentName">
        <component
          :is="column.renderComponentName"
          :row-data="rowData"
          :column="column"
          :thead="thead"
          :actions="actions"
        />
      </div>
      <!-- or it's just a decorated text and not a component -->
      <div v-else v-html="column.renderDecoratorFunction(rowData, thead)"/>
      <!-- we finish up with any field end actions -->
      <OrderingIndicator v-if="thead" ref="ordering" :ordering="column.ordering"/>
      <df-actions
        v-if="!thead && actions.fieldEnd(column.name).length"
        :actions="actions.fieldEnd(column.name)"
        class="actions"
      />
      <df-actions
        v-if="!thead && column.name === '#actions-row_end' && actions.rowEnd.length"
        :actions="actions.rowEnd"
        class="actions"
      />
    </template>
  </div>
</template>

<script lang="ts">
import { computed, defineComponent } from 'vue';

import ActionHandlerMixin from '../actions/action-handler-mixin';
import FilteredActions from '../actions/filtered-actions';
import FormField from '../form/field.vue';

import * as TableCells from './cell-renderers';
import ColumnGroup from './column-group.vue';
import TableColumn from './definitions/column';
import OrderingIndicator from './ordering-indicator.vue';
import RenderMeasured from './render-measure';
import RowTypesEnum from './row-types-enum';

export default /* #__PURE__ */ defineComponent({
  name: 'GenericColumn',
  components: { ColumnGroup, OrderingIndicator, FormField, ...TableCells },
  mixins: [RenderMeasured, ActionHandlerMixin],
  provide() {
    return { payload: computed(() => this.rowData) };
  },
  props: {
    column: { type: TableColumn, required: true },
    rowData: { type: Object, required: true },
    actions: { type: FilteredActions, required: true },
    filterRow: { type: TableColumn, default: null },
    rowType: RowTypesEnum.rowTypeProp(),
  },
  computed: {
    thead() { return RowTypesEnum.isTHead(this.rowType); },
    columnClass() {
      return this.column.renderComponentName === 'ColumnGroup' ? 'column-group' : 'df-col';
    },
  },
  methods: {
    onMeasure(refName: string, maxWidth: number) {
      if (refName === 'column') {
        this.column.setMaxWidth(maxWidth);
      }
    },
    customClass() {
      let res = this.column.CSSClass;
      if (this.thead) res = `${res} ${this.column.CSSClassHead}`.trim();
      return res;
    },
  },
});
</script>

<style scoped>
.actions {
  margin: -.25em 0; /* nullify the df-col margin to make the button align better with the data cells */
}
</style>
