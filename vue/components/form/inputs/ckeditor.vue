<template>
  <v-input v-bind="baseBinds">
    <ckeditor v-model="value" :editor="editor" :config="editorConfig"/>
  </v-input>
</template>

<script>
import ClassicEditor from '@ckeditor/ckeditor5-build-classic';
import CKEditor from '@ckeditor/ckeditor5-vue2';

import TranslationsMixin from '../../util/translations_mixin';

import InputBase from './base';

export default {
  name: 'DFWidgetCKEditor',
  components: { ckeditor: CKEditor.component },
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
