<script setup lang="ts">
import { computed } from 'vue';

import { useTranslations } from '../../util/translations-mixin';

import { BaseEmits, BaseProps, useInputBase } from './base';

interface Props extends BaseProps {}
const props = defineProps<Props>();

interface Emits extends BaseEmits {}
const emits = defineEmits<Emits>();

const { value, baseBinds } = useInputBase(props, emits);

const { gettext } = useTranslations();
const rules = computed<((val: string) => boolean | string)[]>(() => ([
  (val: string) => {
    const regex = /^#?([a-fA-F0-9]{6}[a-fA-F0-9]{0,2})$/;
    return regex.test(val) ? true : gettext('Not a valid hex string.');
  },
]));
</script>

<template>
  <v-text-field
    :id="field.uuid"
    v-model="value"
    type="text"
    variant="underlined"
    :class="field.renderParams.fieldCSSClass"
    :name="field.name"
    :placeholder="field.placeholder"

    :rules="rules"
    :step="field.renderParams.step"
    :size="field.renderParams.size"

    :readonly="field.readOnly"

    v-bind="baseBinds"
    :messages="[]"
  >
    <v-menu
      activator="parent"
      :close-on-content-click="false"
    >
      <v-color-picker v-model="value" mode="hexa"/>
    </v-menu>
  </v-text-field>
</template>
