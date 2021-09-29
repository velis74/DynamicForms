<template>
  <DFWidgetBase :key="fieldKey" :def="def" :data="data" :errors="errors" :show-label-or-help-text="showLabelOrHelpText">
    <input
      v-if="indeterminate"
      :id="def.uuid"
      slot="input"
      v-indeterminate="true"
      :checked="false"
      type="checkbox"
      :class="def.render_params.field_class"
      :name="def.name"
      :aria-describedby="def.help_text && showLabelOrHelpText ? def.name + '-help' : null"
      :readonly="readonly"
      :disabled="def.read_only === true"
      @change="change"
    >
    <input
      v-if="!indeterminate"
      :id="def.uuid"
      slot="input"
      v-indeterminate="false"
      :checked="internalValue"
      type="checkbox"
      :class="def.render_params.field_class"
      :name="def.name"
      :aria-describedby="def.help_text && showLabelOrHelpText ? def.name + '-help' : null"
      :readonly="readonly"
      :disabled="def.read_only === true"
      @change="change"
    >
  </DFWidgetBase>
</template>

<script>
import _ from 'lodash';

import DFWidgetBase from './dfwidgetbase.vue';

export default {
  name: 'DFWidgetCheckbox',
  components: { DFWidgetBase },
  directives: {
    indeterminate: (el, binding) => {
      el.indeterminate = Boolean(binding.value);
    },
  },
  props: {
    def: { type: Object, required: true },
    data: { type: Object, required: true },
    errors: { type: Object, required: true },
    showLabelOrHelpText: { type: Boolean, default: true },
  },
  data() {
    return {
      indeterminate: false,
      readonly: this.def.read_only === true,
      internalValue: false,
      fieldKey: Math.round(Math.random() * 1000),
    };
  },
  computed: {
    value: {
      get: function get() {
        return this.data[this.def.name];
      },
      set: function set(newVal) {
        this.data[this.def.name] = newVal; // eslint-disable-line
        this.$emit('onValueConfirmed', true);
      },
    },
  },
  mounted() {
    this.indeterminate = this.def.allow_null && (this.value === undefined || this.value === null);
    if (this.value) {
      this.internalValue = true;
    }
    if (this.value === undefined || this.value === null) {
      this.internalValue = null;
    }
  },
  methods: {
    change(evt) {
      const oldVal = _.clone(this.internalValue);
      const newVal = evt.currentTarget.checked;
      if (this.def.allow_null) {
        if (oldVal === true) {
          this.indeterminate = true;
          this.internalValue = null;
        } else if ((oldVal === null || oldVal === undefined) && this.indeterminate && newVal) {
          this.indeterminate = false;
          this.internalValue = false;
        } else if (oldVal === false && newVal === true) {
          this.internalValue = true;
          this.indeterminate = false;
        }
        this.fieldKey = Math.round(Math.random() * 1000);
        this.value = _.clone(this.internalValue);
      } else {
        this.value = _.clone(newVal);
      }
    },
  },
};
</script>

<style>
th .position-checkbox-static {
  position: static !important;
  margin-left: 0 !important;
}
</style>
