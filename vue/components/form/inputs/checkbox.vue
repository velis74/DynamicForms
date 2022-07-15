<template>
  <v-checkbox
    v-model="value"
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
  mounted() {
    if (this.value) {
      this.internalValue = true;
    }
    if (this.value === undefined || this.value === null) {
      this.internalValue = null;
    }
  },
  methods: {
    change(newValue) {
      const oldVal = _.clone(this.internalValue);
      console.log('newVal:', newValue, 'oldVal:', oldVal, 'indeterminate:', this.indeterminate);
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
        this.value = _.clone(this.internalValue);
      } else {
        this.value = _.clone(newValue);
      }
      if (oldVal !== this.value) {
        this.$emit('onValueConfirmed', true);
      }
    },
  },
};
</script>
