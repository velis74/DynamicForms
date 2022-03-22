<template>
  <vuetify-input>
    <ckeditor v-model="value" :editor="editor" :config="editorConfig"/>
  </vuetify-input>
<!--    <v-input v-bind="baseBinds">-->
<!--    <ckeditor v-model="value" :editor="editor" :config="editorConfig"/>-->
<!--  </v-input>-->
</template>

<script>
import ClassicEditor from '@ckeditor/ckeditor5-build-classic';
import CKEditor from '@ckeditor/ckeditor5-vue2';

import TranslationsMixin from '../../util/translations_mixin';

import InputBase from './base';
import VuetifyInput from './input_vuetify';

export default {
  name: 'DFWidgetCKEditor',
  components: { ckeditor: CKEditor.component, VuetifyInput },
  mixins: [InputBase, TranslationsMixin],
  data() {
    return {
      editor: ClassicEditor,
      editorConfig: {}, // The configuration of the editor.
    };
  },
};
</script>

<style scoped>

</style>
