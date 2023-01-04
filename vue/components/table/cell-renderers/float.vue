<template>
  <div :key="config.maxDecimals" v-html="displayValue"/>
</template>

<script lang="ts">
import { defineComponent, reactive } from 'vue';

export default /* #__PURE__ */ defineComponent({
  name: 'TableCellFloat',
  props: {
    rowData: { type: Object, required: true },
    column: { type: Object, required: true },
    thead: { type: Boolean, default: false },
  },
  computed: {
    value() { return this.rowData[this.column.name]; },
    config() {
      // find the component that has the rows array. We will abuse that component to store our configuration
      let componentWithRows = this.$parent;
      while (!componentWithRows.rows) componentWithRows = componentWithRows.$parent;

      let config = componentWithRows[`_TableCellFloat_${this.column.name}`];

      // if config does not exist yet or if rows actually changed (table was reprovisioned with another one)
      if (!config || config.orgRows !== componentWithRows.rows) {
        config = reactive({
          maxDecimals: 0,
          decimalChar: 1.1.toLocaleString().substring(1, 2),
          orgRows: componentWithRows.rows,
        });
        componentWithRows[`_TableCellFloat_${this.column.name}`] = config;
      }
      return config;
    },
    displayValue() {
      if (this.value == null) return '';
      if (this.thead) return this.value;

      //  read any existing config and create it if it's not there already
      const config = this.config;
      // Make a presentable value
      let res = this.value.toLocaleString();
      if (res === 'None') return res;
      // fill the value with decimals
      const dpPos = res.indexOf(config.decimalChar);
      const numDecimals = dpPos === -1 ? 0 : res.substring(dpPos + 1).length;
      if (numDecimals > config.maxDecimals) config.maxDecimals = numDecimals;
      if (dpPos === -1) res += config.decimalChar;
      const filler = Array(config.maxDecimals + 1 - numDecimals).join('0');

      if (this.column.renderParams.table_show_zeroes) {
        res += filler;
      } else {
        res += filler ? `<span style="visibility: hidden">${filler}</span>` : '';
      }
      return res;
    },
  },
});
</script>
