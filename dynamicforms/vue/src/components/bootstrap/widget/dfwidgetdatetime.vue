<template>
  <DFWidgetBase :def="def" :data="data" :errors="errors" :show-label-or-help-text="showLabelOrHelpText">
    <datetime slot="input" v-model="value" zone="America/New_York" type="datetime" value-zone="Europe/Moscow"/>
    <div slot="error">{{ value }}</div>
  </DFWidgetBase>
</template>

<script>
import { Datetime } from 'vue-datetime';

import DFWidgetBase from './dfwidgetbase.vue';

export default {
  name: 'DFWidgetDatetime',
  components: { DFWidgetBase, Datetime },
  props: {
    def: { type: Object, required: true },
    data: { type: Object, required: true },
    errors: { type: Object, required: true },
    showLabelOrHelpText: { type: Boolean, default: true },
  },
  computed: {
    inputType() { return this.def.render_params.input_type; },
    maxLength() { return this.def.render_params.max_length || (1 << 24); }, // eslint-disable-line no-bitwise
    isTextArea() { return this.def.textarea === true; },
    value: {
      get: function get() { return this.data[this.def.name]; },
      set: function set(newVal) {
        this.data[this.def.name] = newVal; // eslint-disable-line
      },
    },
  },
  methods: {
    onValueConfirmed(doFilter) {
      this.$emit('onValueConfirmed', doFilter);
    },
  },
};
</script>

<style scoped>
  @import '~vue-datetime/dist/vue-datetime.css';
</style>
