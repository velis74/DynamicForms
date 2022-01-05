<template>
  <div style="display: inline-block" v-html="displayValue"/>
</template>

<script>
import { DateTime } from 'luxon';

import DynamicForms from '../../../dynamicforms';

export default {
  name: 'DFTableCellDatetime',
  props: {
    column: { type: Object, required: true },
    value: { type: null, required: true },
  },
  computed: {
    format() {
      return this.column.render_params && this.column.render_params.table_format ?
        this.column.render_params.table_format : DynamicForms.defaultDatetimeFormat;
    },
    displayValue() {
      return DateTime.fromISO(this.value).toFormat(this.format);
    },
  },
};
</script>

<style scoped>

</style>
