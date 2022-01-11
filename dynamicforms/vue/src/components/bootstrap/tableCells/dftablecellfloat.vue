<template>
  <div style="display: inline-block" v-html="displayValue"/>
</template>

<script>
import Vue from 'vue';

export default {
  name: 'DFTableCellFloat',
  props: {
    row: { type: Object, required: true },
    column: { type: Object, required: true },
    value: { type: null, required: true },
    bodyId: { type: Number, required: true },
  },
  computed: {
    displayValue() {
      if (this.value == null) {
        return '';
      }
      // First, ensure we have the namespace ready
      // eslint-disable-next-line no-return-assign
      ['dynamicforms', 'df-tablecell-float-configs'].reduce((res, val) => (res[val] || (res[val] = {})), window);
      //  read any existing config and create it if it's not there already
      let config = window.dynamicforms['df-tablecell-float-configs'][this.bodyId];
      if (!config) {
        config = Vue.observable({
          max_decimals: 0,
          decimal_char: 1.1.toLocaleString().substr(1, 1),
        });
        window.dynamicforms['df-tablecell-float-configs'][this.bodyId] = config;
      }
      // Make a presentable value
      let res = this.value.toLocaleString();
      if (res === 'None') return res;
      // fill the value with invisible decimals
      const dpPos = res.indexOf(config.decimal_char);
      const numDecimals = dpPos === -1 ? 0 : res.substr(dpPos + 1).length;
      if (numDecimals > config.max_decimals) config.max_decimals = numDecimals;
      if (dpPos === -1) res += config.decimal_char;
      const filler = Array(config.max_decimals + 1 - numDecimals).join('0');

      if (this.column.render_params.table_show_zeroes) res += filler;
      else res += filler ? `<span style="visibility: hidden">${filler}</span>` : '';
      return res;
    },
  },
};
</script>

<style scoped>

</style>
