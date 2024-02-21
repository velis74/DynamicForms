<template>
  <vuetify-input
    :label="baseBinds.label"
    :messages="baseBinds.messages"
    :error-messages="baseBinds['error-messages']"
    :error-count="baseBinds['error-count']"
  >
    <ckeditor v-model="value" :editor="editor" :config="editorConfig"/>
  </vuetify-input>
</template>

<script setup lang="ts">
import { BaseEmits, BaseProps, basePropsDefault, useInputBase } from './base';
import Editor from './ck-editor-custom';
import VuetifyInput from './input-vuetify.vue';

interface Props extends BaseProps {}
const props = withDefaults(defineProps<Props>(), basePropsDefault);

interface Emits extends BaseEmits {}
const emits = defineEmits<Emits>();

const { baseBinds, value } = useInputBase(props, emits);

// data
const editor = Editor;
const editorConfig = {}; // The configuration of the editor.

</script>

<style scoped>

</style>
