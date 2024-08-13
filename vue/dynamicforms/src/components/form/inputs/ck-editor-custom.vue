<template>
  <div class="editor-container">
    <div class="editor-container__editor">
      <div ref="editorElement">
        <ckeditor
          v-if="isLayoutReady"
          v-model="editorData"
          :editor="editor"
          :config="editorConfig"
          @ready="onEditorReady"
        />
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import type { Editor, EditorConfig } from '@ckeditor/ckeditor5-core';
import {
  ClassicEditor, AccessibilityHelp, Alignment, AutoImage, AutoLink, Autosave, BalloonToolbar, BlockQuote,
  Bold, CloudServices, Essentials, GeneralHtmlSupport, Heading, HorizontalLine, ImageBlock, ImageCaption,
  ImageInline, ImageInsertViaUrl, ImageResize, ImageStyle, ImageToolbar, ImageUpload, Indent, IndentBlock,
  Italic, Link, List, MediaEmbed, Paragraph, PasteFromMarkdownExperimental, PasteFromOffice, Autoformat,
  SelectAll, Style, Table, TableCellProperties, TableColumnResize, TableProperties, TableToolbar, Undo,
  HeadingConfig, TextTransformation, Base64UploadAdapter,
} from 'ckeditor5';
import { ref, onMounted, watch } from 'vue';

import { gettext } from '../../util/translations-mixin';

interface Props {
  modelValue: string;
  minHeight: string;
}

const props = withDefaults(defineProps<Props>(), { modelValue: '', minHeight: '7em' });

const emit = defineEmits<{
  (e: 'update:modelValue', value: string): void
}>();

const isLayoutReady = ref(false);
const editorData = ref(props.modelValue);
const editor = ClassicEditor;

const editorToolbarConfig = {
  items: [
    'undo', 'redo', '|',
    'selectAll', '|',
    'heading', 'style', '|',
    'bold', 'italic', '|',
    'horizontalLine', 'link', 'mediaEmbed', 'insertTable', 'blockQuote', '|',
    'alignment', '|',
    'bulletedList', 'numberedList', 'outdent', 'indent', '|',
    'accessibilityHelp',
  ],
  shouldNotGroupWhenFull: false,
};
const editorPlugins = [
  AccessibilityHelp, Alignment, AutoImage, AutoLink, Autosave, BalloonToolbar, BlockQuote, Bold, CloudServices,
  Essentials, GeneralHtmlSupport, Heading, HorizontalLine, ImageBlock, ImageCaption, ImageInline, ImageInsertViaUrl,
  ImageResize, ImageStyle, ImageToolbar, ImageUpload, Indent, IndentBlock, Italic, Link, List, Autoformat,
  MediaEmbed, Paragraph, PasteFromMarkdownExperimental, PasteFromOffice, SelectAll, Style, Table, TableCellProperties,
  TableColumnResize, TableProperties, TableToolbar, Undo, TextTransformation, Base64UploadAdapter,
];
const editorHeadings: HeadingConfig = {
  options: [
    { model: 'paragraph', title: 'Paragraph', class: 'ck-heading_paragraph' },
    { model: 'heading1', view: 'h1', title: 'Heading 1', class: 'ck-heading_heading1' },
    { model: 'heading2', view: 'h2', title: 'Heading 2', class: 'ck-heading_heading2' },
    { model: 'heading3', view: 'h3', title: 'Heading 3', class: 'ck-heading_heading3' },
    { model: 'heading4', view: 'h4', title: 'Heading 4', class: 'ck-heading_heading4' },
    { model: 'heading5', view: 'h5', title: 'Heading 5', class: 'ck-heading_heading5' },
    { model: 'heading6', view: 'h6', title: 'Heading 6', class: 'ck-heading_heading6' },
  ],
};
const editorConfig: EditorConfig = {
  toolbar: editorToolbarConfig,
  plugins: editorPlugins,
  balloonToolbar: ['bold', 'italic', '|', 'link', '|', 'bulletedList', 'numberedList'],
  heading: editorHeadings,
  htmlSupport: {
    allow: [
      { name: /^.*$/, styles: true, attributes: true, classes: true },
    ],
  },
  image: {
    toolbar: [
      'toggleImageCaption', 'imageTextAlternative', '|',
      'imageStyle:inline', 'imageStyle:wrapText', 'imageStyle:breakText', '|',
      'resizeImage',
    ],
  },
  // initialData: '',
  link: {
    addTargetToExternalLinks: true,
    defaultProtocol: 'https://',
    decorators: {
      toggleDownloadable: {
        mode: 'manual',
        label: 'Downloadable',
        attributes: { download: 'file' },
      },
    },
  },
  placeholder: gettext('Type or paste your content here!'),
  style: {
    definitions: [
      { name: 'Article category', element: 'h3', classes: ['category'] },
      { name: 'Title', element: 'h2', classes: ['document-title'] },
      { name: 'Subtitle', element: 'h3', classes: ['document-subtitle'] },
      { name: 'Info box', element: 'p', classes: ['info-box'] },
      { name: 'Side quote', element: 'blockquote', classes: ['side-quote'] },
      { name: 'Marker', element: 'span', classes: ['marker'] },
      { name: 'Spoiler', element: 'span', classes: ['spoiler'] },
      { name: 'Code (dark)', element: 'pre', classes: ['fancy-code', 'fancy-code-dark'] },
      { name: 'Code (bright)', element: 'pre', classes: ['fancy-code', 'fancy-code-bright'] },
    ],
  },
  table: { contentToolbar: ['tableColumn', 'tableRow', 'mergeTableCells', 'tableProperties', 'tableCellProperties'] },
};

onMounted(() => {
  isLayoutReady.value = true;
});

// eslint-disable-next-line @typescript-eslint/no-unused-vars
const onEditorReady = (editorReady: Editor) => {
  // console.log('Editor is ready to use!', editorReady);
};

watch(editorData, (newValue: string) => {
  emit('update:modelValue', newValue);
});

defineExpose({ editorData, onEditorReady });
</script>

<style>
@import 'ckeditor5/ckeditor5.css';
@import url('https://fonts.googleapis.com/css2?family=Oswald&family=PT+Serif:ital,wght@0,400;0,700;1,400&display=swap');
@import url('https://fonts.googleapis.com/css2?family=Lato:ital,wght@0,400;0,700;1,400;1,700&display=swap');

:root {
  /* In addition to this, any v-dialog must also have :retain-focus="false" */
  --ck-z-default: 20000!important;
  --ck-z-modal: calc( var(--ck-z-default) + 20999 );
}

@media print {
  body {
    margin: 0 !important;
  }
}

.editor-container {
  font-family:  'Lato';
  margin-left:  auto;
  margin-right: auto;
}

.ck-content {
  font-family: 'Lato';
  line-height: 1.6;
  word-break:  break-word;
}

.editor-container .editor-container__editor {
  width: 100%;
}

:root .ck-editor__editable_inline {
  min-height: v-bind(minHeight);
}

.ck-content h3.category {
  font-family:    'Oswald';
  font-size:      20px;
  font-weight:    bold;
  color:          #555;
  letter-spacing: 10px;
  margin:         0;
  padding:        0;
}

.ck-content h2.document-title {
  font-family: 'Oswald';
  font-size:   50px;
  font-weight: bold;
  margin:      0;
  padding:     0;
  border:      0;
}

.ck-content h3.document-subtitle {
  font-family: 'Oswald';
  font-size:   20px;
  color:       #555;
  margin:      0 0 1em;
  font-weight: bold;
  padding:     0;
}

.ck-content p.info-box {
  --background-size:  30px;
  --background-color: #e91e63;
  padding:            1.2em 2em;
  border:             1px solid var(--background-color);
  background:         linear-gradient(
                        135deg,
                        var(--background-color) 0%,
                        var(--background-color) var(--background-size),
                        transparent var(--background-size)
                      ),
                      linear-gradient(
                        135deg,
                        transparent calc(100% - var(--background-size)),
                        var(--background-color) calc(100% - var(--background-size)),
                        var(--background-color)
                      );
  border-radius:      10px;
  margin:             1.5em 2em;
  box-shadow:         5px 5px 0 #ffe6ef;
}

.ck-content blockquote.side-quote {
  font-family: 'Oswald';
  font-style:  normal;
  float:       right;
  width:       35%;
  position:    relative;
  border:      0;
  overflow:    visible;
  z-index:     1;
  margin-left: 1em;
}

.ck-content blockquote.side-quote::before {
  content:     '“';
  position:    absolute;
  top:         -37px;
  left:        -10px;
  display:     block;
  font-size:   200px;
  color:       #e7e7e7;
  z-index:     -1;
  line-height: 1;
}

.ck-content blockquote.side-quote p {
  font-size:   2em;
  line-height: 1;
}

.ck-content blockquote.side-quote p:last-child:not(:first-child) {
  font-size:  1.3em;
  text-align: right;
  color:      #555;
}

.ck-content span.marker {
  background: yellow;
}

.ck-content span.spoiler {
  background: #000;
  color:      #000;
}

.ck-content span.spoiler:hover {
  background: #000;
  color:      #fff;
}

.ck-content pre.fancy-code {
  border:        0;
  margin-left:   2em;
  margin-right:  2em;
  border-radius: 10px;
}

.ck-content pre.fancy-code::before {
  content:           '';
  display:           block;
  height:            13px;
  background:        url(data:image/svg+xml;base64,PHN2ZyBmaWxsPSJub25lIiB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHZpZXdCb3g9IjAgMCA1NCAxMyI+CiAgPGNpcmNsZSBjeD0iNi41IiBjeT0iNi41IiByPSI2LjUiIGZpbGw9IiNGMzZCNUMiLz4KICA8Y2lyY2xlIGN4PSIyNi41IiBjeT0iNi41IiByPSI2LjUiIGZpbGw9IiNGOUJFNEQiLz4KICA8Y2lyY2xlIGN4PSI0Ny41IiBjeT0iNi41IiByPSI2LjUiIGZpbGw9IiM1NkM0NTMiLz4KPC9zdmc+Cg==);
  margin-bottom:     8px;
  background-repeat: no-repeat;
}

.ck-content pre.fancy-code-dark {
  background: #272822;
  color:      #fff;
  box-shadow: 5px 5px 0 #0000001f;
}

.ck-content pre.fancy-code-bright {
  background: #dddfe0;
  color:      #000;
  box-shadow: 5px 5px 0 #b3b3b3;
}
</style>
