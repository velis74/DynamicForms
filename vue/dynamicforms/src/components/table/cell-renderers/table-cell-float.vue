<template>
  <div :key="config.maxDecimals" v-html="displayValue"/>
</template>

<script setup lang="ts">
import { computed, inject, reactive } from 'vue';

import TableColumn from '../definitions/column';
import TableRow from '../definitions/row';

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

  let cfg = tableConfig[`_TableCellFloat_${props.column.name}`];

  // if config does not exist yet or if rows actually changed (table was reprovisioned with another one)
  if (!cfg) {
    cfg = reactive({
      maxDecimals: 0,
      decimalChar: 1.1.toLocaleString().substring(1, 2),
    });
    tableConfig[`_TableCellFloat_${props.column.name}`] = cfg;
  }
  return cfg;
});
const displayValue = computed(() => {
  if (value.value == null) return '';
  if (props.thead) return value.value;

  //  read any existing config and create it if it's not there already
  const cfg = config.value;
  // Make a presentable value
  let res = value.value.toLocaleString();
  if (res === 'None') return res;
  // fill the value with decimals
  const dpPos = res.indexOf(cfg.decimalChar);
  const numDecimals = dpPos === -1 ? 0 : res.substring(dpPos + 1).length;
  if (numDecimals > cfg.maxDecimals) cfg.maxDecimals = numDecimals;
  if (dpPos === -1) res += cfg.decimalChar;
  const filler = Array(cfg.maxDecimals + 1 - numDecimals).join('0');

  if (props.column.renderParams.table_show_zeroes) {
    res += filler;
  } else {
    res += filler ? `<span style="visibility: hidden">${filler}</span>` : '';
  }
  return res;
});
</script>
