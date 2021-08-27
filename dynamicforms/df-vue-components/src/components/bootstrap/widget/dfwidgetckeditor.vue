<template>
  <dfwidgetbase :def="def" :data="data" :errors="errors" :showLabelOrHelpText="showLabelOrHelpText">
    <ckeditor slot="input" :editor="editor" v-model="editorData" :config="editorConfig">
    </ckeditor>
  </dfwidgetbase>
</template>

<script>
import CKEditor from '@ckeditor/ckeditor5-vue2';
import ClassicEditor from '@ckeditor/ckeditor5-build-classic';
import dfwidgetbase from './dfwidgetbase.vue';

export default {
  name: 'dfwidgetckeditor',
  props: {
    def: {
      type: Object,
      required: true,
    },
    data: {
      type: Object,
      required: true,
    },
    errors: {
      type: Object,
      required: true,
    },
    showLabelOrHelpText: {
      type: Boolean,
      default: true,
    },
  },
  data() {
    return {
      editor: ClassicEditor,
      editorData: '<p>Content of the editor.</p>',
      editorConfig: {
        // The configuration of the editor.
      },
    };
  },
  components: {
    dfwidgetbase,
    ckeditor: CKEditor.component,
  },
};
</script>

<style scoped>

</style>
