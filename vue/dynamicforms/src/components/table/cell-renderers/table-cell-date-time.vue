<template>
  <div v-html="displayValue"/>
</template>

<script setup lang="ts">
import { DateTime } from 'luxon';
import { computed } from 'vue';

import TableColumn from '../definitions/column';
import TableRow from '../definitions/row';

const props = withDefaults(
  defineProps<{
    rowData: TableRow
    column: TableColumn
    thead: boolean
  }>(),
  { thead: false },
);

const value = computed(() => props.rowData[props.column.name]);
const format = computed(() => props.column.renderParams.table_format || 'dd.MM.yyyy HH:mm:ss');
const displayValue = computed(() => {
  if (props.thead) return value.value;
  return DateTime.fromISO(value.value).toFormat(format.value);
});
</script>
