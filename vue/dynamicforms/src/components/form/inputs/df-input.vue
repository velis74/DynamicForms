<template>
  <df-input
    v-model="value"
    :class="field.renderParams.fieldCSSClass"
    :name="field.name"
    :errors="baseBinds['error-messages']"
    :enabled="!field.readOnly"

    :input-type="inputType"
    :step="field.renderParams.step"
    :min="field.renderParams.min"
    :max="field.renderParams.max"
    v-bind="baseBinds"
  />
</template>

<script setup lang="ts">
import { DfInput } from '@dynamicforms/vuetify-inputs';
import { computed } from 'vue';

import { BaseEmits, BaseProps, useInputBase } from './base';

interface Props extends BaseProps { }
const props = defineProps<Props>();

interface Emits extends BaseEmits { }
const emits = defineEmits<Emits>();

const { value, baseBinds } = useInputBase(props, emits);

const inputType = computed(() => props.field.renderParams.inputType as 'text');

</script>
