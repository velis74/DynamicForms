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

import TranslationsMixin from '../../util/translations_mixin';

import InputBase from './base';

export default {
  name: 'DCheckbox',
  mixins: [InputBase, TranslationsMixin],
  data() {
    return {
      internalValue: false,
      indeterminate: this.field.allowNull && (this.value === undefined || this.value === null),
    };
  },
  computed: {
    boolValue: {
      get: function get() {
        return this.internalValue;
      },
      // eslint-disable-next-line no-unused-vars
      set: function set(newVal) {},
    },
  },
  mounted() {
    if (this.value) {
      this.internalValue = true;
      return;
    }
    if (this.value === undefined || this.value === null) {
      this.internalValue = null;
    } else {
      this.internalValue = false;
    }
  },
  methods: {
    change(newValue) {
      const oldVal = _.clone(this.internalValue);
      if (this.field.allowNull) {
        if (oldVal === true) {
          this.indeterminate = true;
          this.internalValue = null;
        } else if ((oldVal === null || oldVal === undefined) && this.indeterminate && newValue) {
          this.indeterminate = false;
          this.internalValue = false;
        } else if (oldVal === false && newValue === true) {
          this.internalValue = true;
          this.indeterminate = false;
        }
        this.boolValue = _.clone(this.internalValue);
      } else {
        this.boolValue = _.clone(newValue);
      }
      this.payload.setValue(this.boolValue);
    },
  },
};
</script>
