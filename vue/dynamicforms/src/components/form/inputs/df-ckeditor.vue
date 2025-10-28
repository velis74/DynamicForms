<template>
  <df-rtf-editor
    v-model="value"

    :errors="baseBinds['error-messages']"
    :hint="baseBinds.hint"
    :persistent-hint="baseBinds['persistent-hint']"
    :hide-details="baseBinds['hide-details']"
    v-bind="baseBinds"
  />
</template>

<script setup lang="ts">
import { DfRtfEditor } from '@dynamicforms/vuetify-inputs';

import { BaseEmits, BaseProps, basePropsDefault, useInputBase } from './base';

interface Props extends BaseProps {}
const props = withDefaults(defineProps<Props>(), basePropsDefault);

interface Emits extends BaseEmits {}
const emits = defineEmits<Emits>();

const { baseBinds, value } = useInputBase(props, emits);

</script>
