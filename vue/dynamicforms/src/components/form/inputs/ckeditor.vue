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
import {BaseEmits, BaseProps, useInputBase} from "./base-composable";
import VuetifyInput from './input-vuetify.vue';

interface Props extends BaseProps {}
const props = defineProps<Props>();

interface Emits extends BaseEmits {}
const emits = defineEmits<Emits>();

const {} = useInputBase(props, emits);

//data
let editor: ClassicEditor;
let editorConfig: {}; // The configuration of the editor.
</script>

<script lang="ts">
import ClassicEditor from '@ckeditor/ckeditor5-build-classic';
import CKEditor from '@ckeditor/ckeditor5-vue';
import { defineComponent } from 'vue';

import TranslationsMixin from '../../util/translations-mixin';

export default defineComponent({

  //TBD with Adam
  components: { ckeditor: CKEditor.component },
  mixins: [TranslationsMixin],

});
</script>

<style scoped>

</style>
