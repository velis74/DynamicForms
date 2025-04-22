<template>
  <div style="width: 100%;">
    <df-text-area
      v-model="value"
      :class="field.renderParams.fieldCSSClass"
      :name="field.name"
      :errors="baseBinds['error-messages']"
      :enabled="!field.readOnly"

      :rows="3"
      :max-rows="10"
      v-bind="baseBinds"
    />
  </div>
</template>

<script setup lang="ts">
import { DfTextArea } from '@dynamicforms/vuetify-inputs';

import { BaseEmits, BaseProps, useInputBase } from './base';

interface Props extends BaseProps { }
const props = defineProps<Props>();

interface Emits extends BaseEmits { }
const emits = defineEmits<Emits>();

const { value, baseBinds } = useInputBase(props, emits);
</script>
