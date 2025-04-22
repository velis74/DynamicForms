<template>
  <div
    ref="columnsize"
    :class="`${columnClass} ${column.name} text-${column.align} ${customClass()}`"
    :style="computedStyleContainer"
    @click.stop="handleClick"
    @mouseup.right="(event) => callHandler(actions.rowRightClick, { column, event, rowType })"
  >
    <template v-if="rowType === RowTypes.Label">
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
      <OrderingIndicator v-if="thead" ref="ordering" :ordering="column.ordering"/>
    </template>
    <template v-else-if="rowType === RowTypes.Filter">
      <component
        :is="column.renderComponentName"
        v-if="column.renderComponentName && column.renderComponentName === 'ColumnGroup'"
        :row-data="rowData"
        :column="column"
        :thead="thead"
        :actions="actions"
        :filter-definition="filterDefinition"
      />
      <template v-else>
        <FormField
          v-if="filterData?.formFieldInstance"
          :field="filterData?.formFieldInstance"
          :actions="actions"
          :errors="{}"
          style="padding: 0; margin: 0;"
        />
      </template>
    </template>
    <template v-else-if="rowType === RowTypes.Data">
      <df-actions
        v-if="column.name === '#actions-row_start' && actions.rowStart.length"
        :actions="actions.rowStart"
        class="actions"
      />
      <!-- first we render any field start actions -->
      <df-actions
        v-if="actions.fieldStart(column.name).length"
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
        :style="computedStyleValue"
      />
      <!-- or it's just a decorated text and not a component -->
      <div v-else :style="computedStyleValue" v-html="column.renderDecoratorFunction(rowData, thead)"/>
      <!-- we finish up with any field end actions -->
      <df-actions
        v-if="actions.fieldEnd(column.name).length"
        :actions="actions.fieldEnd(column.name)"
        class="actions"
      />
      <df-actions
        v-if="column.name === '#actions-row_end' && actions.rowEnd.length"
        :actions="actions.rowEnd"
        class="actions"
      />
    </template>
    <template v-else>
      <div class="text-warning">Unknown row type! {{ rowType }}</div>
    </template>
  </div>
</template>

<script setup lang="ts">
import { computed, defineComponent, inject, provide, ref } from 'vue';

import Action from '../actions/action';
import { useActionHandler } from '../actions/action-handler-composable';
import FilteredActions from '../actions/filtered-actions';
import FormField from '../form/form-field.vue';
import { interpolate } from '../util/translations-mixin';

import * as TableCells from './cell-renderers';
import ColumnGroup from './column-group.vue';
import TableColumn from './definitions/column';
import TableFilterRow from './definitions/filterrow';
import RowTypes from './definitions/row-types';
import { DfTable } from './namespace';
import OrderingIndicator from './ordering-indicator.vue';
import { useRenderMeasure } from './render-measure';

export interface Props {
  column: TableColumn,
  rowData: Object,
  actions: FilteredActions,
  filterRow?: TableColumn,
  filterDefinition?: TableFilterRow,
}

const props = defineProps<Props>();

const rowType: RowTypes = inject('row-type') as RowTypes;
const thead = computed(() => RowTypes.isTHead(rowType));
const columnClass = computed(
  () => (props.column.renderComponentName === 'ColumnGroup' ? 'column-group' : 'df-col'),
);
const payload = computed(() => props.rowData);

const { callHandler } = useActionHandler();

// Checks if max width is set. if yes, it gets the value; if no, returns the empty string
// Create a ref to store the maxWidthStyle
const computedStyleContainer = computed(() => {
  if (props.column.renderParams?.max_width) {
    return interpolate('max-width: %(width)s; display: inline-flex;', { width: props.column.renderParams.max_width });
  }
  return ''; // Empty string if max_width is not defined
});
const computedStyleValue = computed(() => {
  if (props.column.renderParams?.max_width) {
    let retStyle = interpolate('max-width: %(width)s;', { width: props.column.renderParams.max_width });
    if (!props.filterDefinition) {
      retStyle += ' overflow: hidden; text-overflow: ellipsis;';
    }
    return retStyle;
  }
  return ''; // Empty string if max_width is not defined
});

function onMeasure(refName: string, maxWidth: number) {
  if (refName === 'columnsize' && Number.isFinite(maxWidth)) {
    props.column.setMaxWidth(maxWidth);
  }
}

const filterData = computed(() => (props.filterDefinition ?
  props.filterDefinition.columns[props.column.name] || new TableColumn({} as DfTable.ColumnJSON, []) :
  null));

function customClass(): string {
  let res = props.column.CSSClass;
  if (thead.value) res = `${res} ${props.column.CSSClassHead}`.trim();
  return res;
}

provide('payload', payload);

function handleClick(event: any) {
  callHandler(new Action({
    name: 'select',
    label: 'Select',
    icon: 'thumbs-down-outline',
    position: 'ROW_CLICK',
  }));
  callHandler(props.actions.rowClick, { column: props.column, event, rowType });
}

const columnsize = ref();
const ordering = ref();

useRenderMeasure(onMeasure, { columnsize, ordering });
</script>
<script lang="ts">
export default defineComponent<Props>({
  name: 'GenericColumn',
  components: { ColumnGroup, OrderingIndicator, FormField, ...TableCells },
});
</script>

<style scoped>
.actions {
  margin: -.25em 0; /* nullify the df-col margin to make the button align better with the data cells */
}
</style>
