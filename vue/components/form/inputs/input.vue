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
    :hint="field.helpText"
    :label="field.label"

    @keyup.enter="onValueConfirmed(true)"
    @input="onValueConfirmed(false)"
    @change="onValueConfirmed(false)"
  />
</template>

<script>
/**
 * TODO: vuetify number input will store a string as value.
 * TODO: It won't store anything if number is entered incorrectly, e.g. by using the wrong decimal separator
 */
import TranslationsMixin from '../../util/translations_mixin';

import InputBase from './base';

export default {
  name: 'DInput',
  mixins: [InputBase, TranslationsMixin],
  computed: {
    inputType() {
      return this.field.renderParams.inputType;
    },
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
      return res;
    },
  },
  methods: {
    onValueConfirmed(doFilter) {
      this.$emit('onValueConfirmed', doFilter);
    },
  },
};
</script>
