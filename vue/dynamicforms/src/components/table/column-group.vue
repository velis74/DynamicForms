<template>
  <div>
    <div v-for="(row, row_index) in column.rows" :key="row_index" class="sub-row">
      <GenericColumn
        v-for="field in row.fields"
        :key="field.name"
        :column="field"
        :row-data="rowData"
        :actions="actions"
        :filter-definition="filterDefinition"
      />
    </div>
  </div>
</template>

<script setup lang="ts">
import FilteredActions from '../actions/filtered-actions';

import TableFilterRow from './definitions/filterrow';
import { ColumnGroup } from './definitions/responsive-layout';

defineProps<{
  column: ColumnGroup,
  rowData: Record<string, any>,
  actions: FilteredActions,
  filterDefinition?: TableFilterRow,
}>();
</script>
<script lang="ts">
export default { name: 'ColumnGroup' };
</script>
