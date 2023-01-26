<template>
  <div v-html="displayValue"/>
</template>

<script lang="ts">
import { DateTime } from 'luxon';

export default {
  name: 'TableCellDateTime',
  props: {
    rowData: { type: Object, required: true },
    column: { type: Object, required: true },
    thead: { type: Boolean, default: false },
  },
  computed: {
    value() { return this.rowData[this.column.name]; },
    format() {
      return this.column.renderParams.table_format || 'dd.MM.yyyy HH:mm:ss';
    },
    displayValue() {
      if (this.thead) return this.value;
      return DateTime.fromISO(this.value).toFormat(this.format);
    },
  },
};
</script>
