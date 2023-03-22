<template>
  <div>
    <div v-for="(row, row_index) in column.rows" :key="row_index" class="sub-row">
      <GenericColumn
        v-for="field in row.fields"
        :key="field.name"
        :column="field"
        :row-data="rowData"
        :row-type="rowType"
        :thead="thead"
        :actions="actions"
      />
    </div>
  </div>
</template>

<script setup lang="ts">
import { computed } from 'vue';

import FilteredActions from '../actions/filtered-actions';

import TableColumn from './definitions/column';
import RowTypesEnum from './row-types-enum';

const props = defineProps({
  column: { type: TableColumn, required: true },
  rowData: { type: Object, required: true },
  actions: { type: FilteredActions, required: true },
  rowType: RowTypesEnum.rowTypeProp(),
});

const thead = computed(() => RowTypesEnum.isTHead(props.rowType));
</script>
<script lang="ts">
export default { name: 'ColumnGroup' };
</script>
