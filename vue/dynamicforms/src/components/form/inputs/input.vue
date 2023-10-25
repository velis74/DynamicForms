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

<script setup lang="ts">
import {BaseEmits, BaseProps, useInputBase} from "./base-composable";
import {computed} from "vue";

interface Props extends BaseProps {}
const props = defineProps<Props>();

interface Emits extends BaseEmits {}
const emits = defineEmits<Emits>();

const {value, isValidNumber, isNumber} = useInputBase(props, emits);

//computed
const inputType = computed(() => {
  return props.field.renderParams.inputType;
})

const rules = computed(() => {
  const res = [];
  const rp = props.field.renderParams;
  res.push((value: string) => ((rp.pattern == null || String(value).match(rp.pattern)) ?
    true : `${value} does not match ${rp.pattern}`));
  res.push(
    (value: string) => ((String(value).length >= rp.minLength) ? true : `len(${value}) < ${rp.minLength}`),
  );
  res.push(
    (value: string) => ((String(value).length <= rp.maxLength) ? true : `len(${value}) > ${rp.maxLength}`),
  );
  if (isNumber) {
    res.push((value: number) => ((rp.min == null || value >= rp.min) ? true : `${value} < ${rp.min}`));
    res.push((value: number) => ((rp.max == null || value <= rp.max) ? true : `${value} > ${rp.max}`));
    // if null is allowed then null and undefined should not trigger invalid number
    res.push(
      (value: number) => (isValidNumber(value) || (props.field.allowNull && value == null) ?
        true :
        'Not a valid number'),
    );
  }
  return res;
})

</script>

<script lang="ts">
import { defineComponent } from 'vue';

import TranslationsMixin from '../../util/translations-mixin';

export default /* #__PURE__ */ defineComponent({
  mixins: [TranslationsMixin],
});
</script>
