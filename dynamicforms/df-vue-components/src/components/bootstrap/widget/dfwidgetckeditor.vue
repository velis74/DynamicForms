<template>
  <dfwidgetbase :def="def" :data="data">
    <ckeditor slot="input" :editor="editor" v-model="editorData" :config="editorConfig">
    </ckeditor>
  </dfwidgetbase>
</template>

<script>
import dfwidgetbase from '@/components/bootstrap/widget/dfwidgetbase.vue';
import CKEditor from '@ckeditor/ckeditor5-vue2';
import ClassicEditor from '@ckeditor/ckeditor5-build-classic';

export default {
  name: 'widgetckeditor',
  props: ['def', 'data'],
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
