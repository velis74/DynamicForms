<template>
  <vuetify-input
    :label="baseBinds.label"
    :messages="baseBinds.messages"
    :error-messages="baseBinds['error-messages']"
    :error-count="baseBinds['error-count']"
  >
    <ck-editor-custom ref="$editor" v-model="value"/>
  </vuetify-input>
</template>

<script setup lang="ts">
import { BaseEmits, BaseProps, basePropsDefault, useInputBase } from './base';
import CkEditorCustom from './ck-editor-custom.vue';
import VuetifyInput from './input-vuetify.vue';

interface Props extends BaseProps {}
const props = withDefaults(defineProps<Props>(), basePropsDefault);

interface Emits extends BaseEmits {}
const emits = defineEmits<Emits>();

const { baseBinds, value } = useInputBase(props, emits);

</script>
