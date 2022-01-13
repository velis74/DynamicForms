<template>
  <DFWidgetBase :def="def" :data="data" :errors="errors" :show-label-or-help-text="showLabelOrHelpText">
    <ckeditor slot="input" v-model="value" :editor="editor" :config="editorConfig"/>
  </DFWidgetBase>
</template>

<script>
import ClassicEditor from '@ckeditor/ckeditor5-build-classic';
import CKEditor from '@ckeditor/ckeditor5-vue2';

import DFWidgetBase from './dfwidgetbase.vue';

export default {
  name: 'DFWidgetCKEditor',
  components: {
    DFWidgetBase, ckeditor: CKEditor.component,
  },
  props: {
    def: { type: Object, required: true },
    data: { type: Object, required: true },
    errors: { type: Object, required: true },
    showLabelOrHelpText: { type: Boolean, default: true },
  },
  data() {
    return {
      editor: ClassicEditor,
      editorConfig: {
        // The configuration of the editor.
      },
    };
  },
  computed: {
    value: {
      get: function get() { return this.data[this.def.name]; },
      set: function set(newVal) {
        this.data[this.def.name] = newVal; // eslint-disable-line
      },
    },
  },
};
</script>

<style scoped>

</style>
