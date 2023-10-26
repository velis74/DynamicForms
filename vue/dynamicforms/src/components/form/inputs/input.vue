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
import { computed } from 'vue';

import { BaseEmits, BaseProps, useInputBase } from './base-composable';

interface Props extends BaseProps {}
const props = defineProps<Props>();

interface Emits extends BaseEmits {}
const emits = defineEmits<Emits>();

const { value, isValidNumber, isNumber, baseBinds } = useInputBase(props, emits);

// computed
const inputType = computed(() => props.field.renderParams.inputType);

const rules = computed(() => {
  const res = [];
  const rp = props.field.renderParams;
  res.push((val: string) => ((rp.pattern == null || String(val).match(rp.pattern)) ?
    true : `${val} does not match ${rp.pattern}`));
  res.push(
    (val: string) => ((String(val).length >= rp.minLength) ? true : `len(${val}) < ${rp.minLength}`),
  );
  res.push(
    (val: string) => ((String(val).length <= rp.maxLength) ? true : `len(${val}) > ${rp.maxLength}`),
  );
  if (isNumber.value) {
    res.push((val: number) => ((rp.min == null || val >= rp.min) ? true : `${val} < ${rp.min}`));
    res.push((val: number) => ((rp.max == null || val <= rp.max) ? true : `${val} > ${rp.max}`));
    // if null is allowed then null and undefined should not trigger invalid number
    res.push(
      (val: number) => (isValidNumber(val) || (props.field.allowNull && val == null) ?
        true :
        'Not a valid number'),
    );
  }
  return res;
});

</script>
