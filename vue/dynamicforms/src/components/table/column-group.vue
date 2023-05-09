<template>
  <div>
    <div v-for="(row, row_index) in column.rows" :key="row_index" class="sub-row">
      <GenericColumn
        v-for="field in row.fields"
        :key="field.name"
        :column="field"
        :row-data="rowData"
        :actions="actions"
      />
    </div>
  </div>
</template>

<script setup lang="ts">
import FilteredActions from '../actions/filtered-actions';

import { ColumnGroup } from './definitions/responsive-layout';

defineProps<{
  column: ColumnGroup,
  rowData: Record<string, any>,
  actions: FilteredActions,
}>();
</script>
<script lang="ts">
export default { name: 'ColumnGroup' };
</script>
