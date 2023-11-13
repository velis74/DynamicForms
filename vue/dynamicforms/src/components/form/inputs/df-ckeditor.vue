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
import ClassicEditor from '@ckeditor/ckeditor5-build-classic';
import CKEditor from '@ckeditor/ckeditor5-vue';

import { BaseEmits, BaseProps, basePropsDefault, useInputBase } from './base';
import VuetifyInput from './input-vuetify.vue';

const ckeditor = CKEditor.component;

interface Props extends BaseProps {}
const props = withDefaults(defineProps<Props>(), basePropsDefault);

interface Emits extends BaseEmits {}
const emits = defineEmits<Emits>();

const { baseBinds, value } = useInputBase(props, emits);

// data
const editor = ClassicEditor;
const editorConfig = {}; // The configuration of the editor.

</script>

<style scoped>

</style>
