<template>
  <df-date-time
    v-model="value"

    :label="baseBinds.label"
    :errors="baseBinds['error-messages']"
    :hint="baseBinds.hint"
    :persistent-hint="baseBinds['persistent-hint']"
    :clearable="true"
    :input-type="inputType"
  />
</template>

<script setup lang="ts">
import { DfDateTime } from '@dynamicforms/vuetify-inputs';
import { computed } from 'vue';

import { BaseEmits, BaseProps, basePropsDefault, useInputBase } from './base';

interface Props extends BaseProps {}
const props = withDefaults(defineProps<Props>(), basePropsDefault);

interface Emits extends BaseEmits {
  (e: 'onValueConfirmed', value: any): any
}
const emits = defineEmits<Emits>();

const { value, baseBinds } = useInputBase(props, emits);

// computed
const inputType = computed(() => props.field.renderParams.inputType as 'datetime' | 'date' | 'time' | undefined);
</script>
