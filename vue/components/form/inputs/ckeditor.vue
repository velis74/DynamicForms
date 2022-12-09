<template>
  <vuetify-input
    :label="baseBinds.label"
    :messages="baseBinds.messages"
    :error-messages="baseBinds['error-messages']"
    :error-count="baseBinds['error-count']"
  >
  <!--    <ckeditor v-model="value" :editor="editor" :config="editorConfig"/>-->
  TODO
  </vuetify-input>
</template>

<script>
// import ClassicEditor from '@ckeditor/ckeditor5-build-classic';
// import CKEditor from '@ckeditor/ckeditor5-vue2';

import TranslationsMixin from '../../util/translations-mixin';

import InputBase from './base';
// import VuetifyInput from './input-vuetify';

export default {
  name: 'DFWidgetCKEditor',
  // components: { ckeditor: CKEditor.component, VuetifyInput },
  mixins: [InputBase, TranslationsMixin],
  // data() {
  //   return {
  //     editor: ClassicEditor,
  //     editorConfig: {}, // The configuration of the editor.
  //   };
  // },
};
</script>

<style scoped>

</style>
