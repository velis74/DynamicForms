<template>
  <div>
    <div v-for="(row, row_index) in column.rows" :key="row_index" class="sub-row">
      <GenericColumn
        v-for="field in row.fields"
        :key="field.name"
        :column="field"
        :row-data="rowData"
        :thead="thead"
        :actions="actions"
        :row-type="rowType"
      />
    </div>
  </div>
</template>

<script setup lang="ts">
import { computed, getCurrentInstance } from 'vue';

import FilteredActions from '../actions/filtered-actions';

import { ColumnGroup } from './definitions/responsive-layout';
import RowTypesEnum from './row-types-enum';

const props = defineProps({
  column: { type: ColumnGroup, required: true },
  rowData: { type: Object, required: true },
  actions: { type: FilteredActions, required: true },
  rowType: RowTypesEnum.rowTypeProp(),
});

const rowType = computed(() => (getCurrentInstance()!.parent?.props.rowType));
const thead = computed(() => RowTypesEnum.isTHead(props.rowType));
</script>
<script lang="ts">
export default { name: 'ColumnGroup' };
</script>
