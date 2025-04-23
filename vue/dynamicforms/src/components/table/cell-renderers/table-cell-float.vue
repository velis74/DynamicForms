<template>
  <div :key="config.maxDecimals" class="number-cell" :class="{ 'show-zeroes': showZeroes }">
    {{ displayValue.main }}<span class="decimals">{{ displayValue.filler }}</span>
  </div>
</template>

<script setup lang="ts">
import { computed, inject, reactive } from 'vue';

import TableColumn from '../definitions/column';
import TableRow from '../definitions/row';

interface DisplayValue {
  main: string;
  filler: string;
}

//  name: 'TableCellFloat',
const props = withDefaults(
  defineProps<{
    rowData: TableRow
    column: TableColumn
    thead: boolean
  }>(),
  { thead: false },
);

const value = computed(() => props.rowData[props.column.name]);
const config = computed(() => {
  const tableConfig: any = inject('table-config'); // provided by table.ts

  let cfg;
  if (tableConfig) {
    cfg = tableConfig[`_TableCellFloat_${props.column.name}`];
  }

  // if config does not exist yet or if rows actually changed (table was reprovisioned with another one)
  if (!cfg) {
    cfg = reactive({
      maxDecimals: 0,
      decimalChar: 1.1.toLocaleString().substring(1, 2),
    });
    if (tableConfig) {
      tableConfig[`_TableCellFloat_${props.column.name}`] = cfg;
    }
  }
  return cfg;
});
const showZeroes = computed(() => props.column.renderParams.table_show_zeroes ?? false);

const displayValue = computed((): DisplayValue => {
  if (value.value == null) return { main: '', filler: '' };
  if (props.thead) return { main: value.value, filler: '' };

  //  read any existing config and create it if it's not there already
  const cfg = config.value;
  // Make a presentable value
  let res = value.value.toLocaleString();
  if (res === 'None') return { main: res, filler: '' };

  // fill the value with decimals
  const dpPos = res.indexOf(cfg.decimalChar);
  const numDecimals = dpPos === -1 ? 0 : res.substring(dpPos + 1).length;

  if (numDecimals > cfg.maxDecimals) cfg.maxDecimals = numDecimals;

  // When only whole numbers are in dataset, don't add decimal and decimal digits
  if (dpPos === -1 && cfg.maxDecimals === 0) return { main: res, filler: '' };

  if (dpPos === -1) res += cfg.decimalChar;
  const filler = Array(cfg.maxDecimals + 1 - numDecimals).join('0');

  return { main: res, filler };
});
</script>
<style scoped>
.number-cell {
  text-align: right;
}

.decimals {
  visibility: hidden;
}

.show-zeroes .decimals {
  visibility: visible;
  opacity: .6;
}
</style>
