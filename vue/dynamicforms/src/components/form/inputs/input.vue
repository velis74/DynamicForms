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
import _ from 'lodash';
import { computed } from 'vue';

import { BaseEmits, BaseProps, useInputBase } from './base';

interface Props extends BaseProps {}
const props = defineProps<Props>();

interface Emits extends BaseEmits {}
const emits = defineEmits<Emits>();

const { baseBinds } = useInputBase(props, emits);

// computed
const isNumber = computed(() => props.field.renderParams.inputType === 'number');
function isValidNumber(num: any) {
  const notValidValues: any[] = [undefined, Number.NaN];
  if (!props.field.allowNull) {
    notValidValues.push(null);
    notValidValues.push('');
  }
  return !_.includes(notValidValues, num) && !Number.isNaN(num) &&
    !_.includes(String(num), ',') && !_.endsWith(String(num), ',');
}

function handleNumberInput(newValue: any) {
  if (isNumber.value && isValidNumber(newValue)) {
    emits('update:modelValue', newValue ? Number(newValue) : undefined);
    return;
  }
  emits('update:modelValue', newValue);
}

const value = computed({
  get(): any {
    return props.modelValue;
  },
  set(newValue: any) {
    handleNumberInput(newValue);
    emits('update:modelValue', newValue);
  },
});

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
