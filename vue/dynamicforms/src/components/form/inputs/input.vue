<template>
  <v-text-field
    :id="field.uuid"
    v-model="value"
    :type="inputType"
    variant="underlined"
    :class="field.renderParams.fieldCSSClass"
    :name="field.name"
    :placeholder="field.placeholder"

    :rules="rules"
    :step="field.renderParams.step"
    :size="field.renderParams.size"

    :readonly="field.readOnly"
    :disabled="field.readOnly"

    v-bind="baseBinds"
    :messages="[]"
  />
</template>

<script lang="ts">
import { defineComponent } from 'vue';

import TranslationsMixin from '../../util/translations-mixin';

import InputBase from './base';

export default /* #__PURE__ */ defineComponent({
  name: 'DInput',
  mixins: [InputBase, TranslationsMixin],
  computed: {
    inputType() { return this.field.renderParams.inputType; },
    rules() {
      const res = [];
      const rp = this.field.renderParams;
      if (rp.pattern) {
        res.push((value: any) => (String(value).match(rp.pattern) ? true : `${value} does not match ${rp.pattern}`));
      }
      if (rp.min) res.push((value: number) => ((value >= rp.min) ? true : `${value} < ${rp.min}`));
      if (rp.max) res.push((value: number) => ((value >= rp.min) ? true : `${value} > ${rp.min}`));
      if (rp.minLength) {
        res.push(
          (value: string) => ((String(value).length >= rp.minLength) ? true : `len(${value}) < ${rp.minLength}`),
        );
      }
      if (rp.maxLength) {
        res.push(
          (value: string) => ((String(value).length <= rp.maxLength) ? true : `len(${value}) > ${rp.maxLength}`),
        );
      }
      if (this.isNumber) {
        // if null is allowed then null and undefined should not trigger invalid number
        res.push(
          (value: number) => (this.isValidNumber(value) || (this.field.allowNull && value == null) ?
            true :
            'Not a valid number'),
        );
      }
      return res;
    },
  },
});
</script>
