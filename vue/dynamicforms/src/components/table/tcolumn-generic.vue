<template>
  <div
    ref="columnsize"
    :class="`${columnClass} ${column.name} text-${column.align} ${customClass()}`"
    @click.stop="(event) => callHandler(actions.rowClick, { column, event, rowType })"
    @mouseup.right="(event) => callHandler(actions.rowRightClick, { column, event, rowType })"
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
      <df-actions
        v-if="!thead && actions.fieldStart(column.name).length"
        :actions="actions.fieldStart(column.name)"
        class="actions"
      />
      <!-- then the field component itself -->
      <component
        :is="column.renderComponentName"
        v-if="column.renderComponentName"
        :row-data="rowData"
        :column="column"
        :thead="thead"
        :actions="actions"
      />
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

<script setup lang="ts">
import { computed, defineComponent, inject, provide, ref } from 'vue';

import { useActionHandler } from '../actions/action-handler-composable';
import FilteredActions from '../actions/filtered-actions';
import FormField from '../form/form-field.vue';

import * as TableCells from './cell-renderers';
import ColumnGroup from './column-group.vue';
import TableColumn from './definitions/column';
import RowTypes from './definitions/row-types';
import OrderingIndicator from './ordering-indicator.vue';
import { useRenderMeasure } from './render-measure';

const props = defineProps<{
  column: TableColumn,
  rowData: Object,
  actions: FilteredActions,
  filterRow?: TableColumn,
}>();

const rowType: RowTypes = inject('row-type') as RowTypes;
const thead = computed(() => RowTypes.isTHead(rowType));
const columnClass = computed(
  () => (props.column.renderComponentName === 'ColumnGroup' ? 'column-group' : 'df-col'),
);
const payload = computed(() => props.rowData);

const { callHandler } = useActionHandler();

function onMeasure(refName: string, maxWidth: number) {
  if (refName === 'columnsize' && Number.isFinite(maxWidth)) {
    props.column.setMaxWidth(maxWidth);
  }
}

function customClass(): string {
  let res = props.column.CSSClass;
  if (thead.value) res = `${res} ${props.column.CSSClassHead}`.trim();
  return res;
}

provide('payload', payload);

const columnsize = ref();
const ordering = ref();

useRenderMeasure(onMeasure, { columnsize, ordering });
</script>
<script lang="ts">
export default defineComponent({
  name: 'GenericColumn',
  components: { ColumnGroup, OrderingIndicator, FormField, ...TableCells },
});
</script>

<style scoped>
.actions {
  margin: -.25em 0; /* nullify the df-col margin to make the button align better with the data cells */
}
</style>
