<template>
  <df-check
    v-model="value"
    :allow-null="props.field.allowNull"
    :class="field.renderParams.fieldCSSClass"
    :name="field.name"
    :enabled="!field.readOnly"
    v-bind="baseBinds"
  />
</template>

<script setup lang="ts">
import { DfCheckbox as DfCheck } from '@dynamicforms/vuetify-inputs';

import { BaseEmits, BaseProps, basePropsDefault, useInputBase } from './base';

interface Props extends BaseProps {}
const props = withDefaults(defineProps<Props>(), basePropsDefault);

interface Emits extends BaseEmits {}
const emits = defineEmits<Emits>();

const { value, baseBinds } = useInputBase(props, emits);
</script>
