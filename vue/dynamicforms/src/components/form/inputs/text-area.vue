<template>
  <div style="width: 100%;">
    <v-textarea
      :id="field.uuid"
      v-model="value"
      :type="inputType"
      variant="underlined"
      :class="field.renderParams.fieldCSSClass"
      :name="field.name"
      :placeholder="field.placeholder"
      :persistent-placeholder="Boolean(field.placeholder && field.placeholder.length > 0)"

      :minlength="minLength"
      :maxlength="maxLength"
      :step="field.renderParams.step"
      :size="field.renderParams.size"

      :readonly="field.readOnly"
      :disabled="field.readOnly"
      :label="baseBinds.label"
      :error-messages="baseBinds['error-messages']"
      :error-count="baseBinds['error-count']"
      :hint="baseBinds.hint"
      :persistent-hint="baseBinds['persistent-hint']"
      :hide-details="baseBinds['hide-details']"
    />
  </div>
</template>

<script setup lang="ts">
import { computed } from 'vue';

import { BaseEmits, BaseProps, useInputBase } from './base';

interface Props extends BaseProps {
}

const props = defineProps<Props>();

interface Emits extends BaseEmits {
}

const emits = defineEmits<Emits>();

const { baseBinds } = useInputBase(props, emits);

// computed
const inputType = computed(() => props.field.renderParams.inputType);

const minLength = computed(() => props.field.renderParams.minLength);

const maxLength = computed(() => props.field.renderParams.maxLength);

const value = computed({
  get(): any {
    return props.modelValue;
  },
  set(newVal: string) {
    emits('update:modelValue', newVal);
  },
});

</script>
