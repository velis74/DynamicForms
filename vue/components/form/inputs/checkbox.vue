<template>
  <v-checkbox
    v-model="boolValue"
    :indeterminate="indeterminate"
    :false-value="false"
    :true-value="true"
    :class="field.renderParams.fieldCSSClass"
    :name="field.name"
    :readonly="field.readOnly"
    :disabled="field.readOnly"
    v-bind="baseBinds"
    @change="change"
  />
</template>

<script>
import _ from 'lodash';

import TranslationsMixin from '../../util/translations-mixin';

import InputBase from './base';

export default {
  name: 'DCheckbox',
  mixins: [InputBase, TranslationsMixin],
  data() { return { internalValue: false }; },
  computed: {
    indeterminate() {
      return this.field.allowNull && (this.internalValue == null);
    },
    boolValue: {
      get: function get() { return this.internalValue; },
      set: function set(newVal) { console.log(this.value, newVal); },
    },
  },
  mounted() {
    if (this.value) {
      this.internalValue = true;
    } else if (this.value == null) {
      this.internalValue = null;
    } else {
      this.internalValue = false;
    }
  },
  methods: {
    change() {
      const oldVal = _.clone(this.internalValue);
      if (oldVal === true) {
        this.internalValue = this.field.allowNull ? null : false;
      } else if (oldVal == null) {
        this.internalValue = false;
      } else if (oldVal === false) this.internalValue = true;
      this.payload.setValue(this.internalValue);
    },
  },
};
</script>
