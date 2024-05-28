<template>
  <vuetify-input
    :label="baseBinds.label"
    :messages="baseBinds.messages"
    :error-messages="baseBinds['error-messages']"
    :error-count="baseBinds['error-count']"
  >
    <ckeditor ref="$editor" v-model="value" :editor="editor" :config="editorConfig"/>
  </vuetify-input>
</template>

<script setup lang="ts">
import '@velis/ckeditor-dist/styles.css';
import Editor from '@velis/ckeditor-dist';
import { computed, ref } from 'vue';

import { BaseEmits, BaseProps, basePropsDefault, useInputBase } from './base';
import VuetifyInput from './input-vuetify.vue';

interface Props extends BaseProps {}
const props = withDefaults(defineProps<Props>(), basePropsDefault);

interface Emits extends BaseEmits {}
const emits = defineEmits<Emits>();

const { baseBinds, value } = useInputBase(props, emits);

const $editor = ref(null);

// data
const editor = Editor;
// The configuration of the editor.
const editorConfig = computed(() => ({}));

</script>
