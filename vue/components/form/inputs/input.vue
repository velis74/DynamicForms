<template>
  <v-text-field
    :id="field.uuid"
    v-model="value"
    :type="inputType"
    :class="field.renderParams.fieldCSSClass"
    :name="field.name"
    :placeholder="field.placeholder"

    :rules="rules"
    :step="field.renderParams.step"
    :size="field.renderParams.size"

    :readonly="field.readOnly"
    :disabled="field.readOnly"

    v-bind="baseBinds"
  />
</template>

<script>
import TranslationsMixin from '../../util/translations-mixin';

import InputBase from './base';

export default {
  name: 'DInput',
  mixins: [InputBase, TranslationsMixin],
  computed: {
    inputType() { return this.field.renderParams.inputType; },
    rules() {
      const res = [];
      const rp = this.field.renderParams;
      if (rp.pattern) {
        res.push((value) => (String(value).match(rp.pattern) ? true : `${value} does not match ${rp.pattern}`));
      }
      if (rp.min) res.push((value) => ((value >= rp.min) ? true : `${value} < ${rp.min}`));
      if (rp.max) res.push((value) => ((value >= rp.min) ? true : `${value} > ${rp.min}`));
      if (rp.minLength) {
        res.push((value) => ((String(value).length >= rp.minLength) ? true : `len(${value}) < ${rp.minLength}`));
      }
      if (rp.maxLength) {
        res.push((value) => ((String(value).length <= rp.maxLength) ? true : `len(${value}) > ${rp.maxLength}`));
      }
      if (this.isNumber) {
        res.push((value) => (this.isValidNumber(value) ? true : 'Not a valid number'));
      }
      return res;
    },
  },
};
</script>
