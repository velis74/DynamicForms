<template>
  <df-color
    v-model="value"
    :class="field.renderParams.fieldCSSClass"
    :name="field.name"
    :errors="baseBinds['error-messages']"
    :enabled="!field.readOnly"
    v-bind="baseBinds"
  />
</template>
<script setup lang="ts">
import { DfColor } from '@dynamicforms/vuetify-inputs';

import { BaseEmits, BaseProps, useInputBase } from './base';

interface Props extends BaseProps {}
const props = defineProps<Props>();

interface Emits extends BaseEmits {}
const emits = defineEmits<Emits>();

const { value, baseBinds } = useInputBase(props, emits);
</script>
