<template>
  <v-input v-bind="baseBinds">
    <div class="input-group">
      <input
        ref="file"
        :key="fileInputKey"
        type="file"
        :readonly="field.readOnly"
        :disabled="field.readOnly"
        :name="field.name"
        @change="selectFile"
      >
    </div>
    <div>
      <div v-if="currentFile" class="progress" style="margin-top: 0.3em;">
        <div
          class="progress-bar progress-bar-info progress-bar-striped"
          role="progressbar"
          :aria-valuenow="progress"
          aria-valuemin="0"
          aria-valuemax="100"
          :style="{ width: progress + '%' }"
        >
          {{ progress }}%
        </div>
      </div>
      <div>
        <div v-if="showFileOnServer">
          {{ getFileName(currentFile ? currentFile.name : value) }}
          <button
            type="button"
            class="close"
            aria-label="Close"
            style="color: red"
            @click="removeFile"
          >
            <span aria-hidden="true">&times;</span>
          </button>
        </div>
      </div>
    </div>
  </v-input>
</template>

<script>
/**
 * TODO: the field does not look like a Vuetify field: it is not underlined, label is on left
 * TODO: the field has a different mechanism for clearing than e.g. datetime: this one's using x while the other
 *   is using IonIcon
 */
import _ from 'lodash';

import apiClient from '../../util/api_client';
import TranslationsMixin from '../../util/translations_mixin';

import InputBase from './base';

export default {
  name: 'DFile',
  mixins: [InputBase, TranslationsMixin],
  data() {
    return {
      currentFile: undefined,
      progress: 0,
      showFileOnServer: false,
      fileInputKey: Math.round(Math.random() * 1000),
    };
  },
  mounted() {
    this.showFileOnServer = !!_.clone(this.value);
  },
  methods: {
    getFileName(filePath) {
      // returns just the filename without any path
      return !filePath ? filePath : filePath.replace(/^.*[\\/]/, '');
    },
    selectFile() {
      this.upload();
    },
    removeFile() {
      this.value = null;  // eslint-disable-line
      this.progress = 0;
      this.fileInputKey = Math.round(Math.random() * 1000);
      this.showFileOnServer = false;
      this.currentFile = undefined;
    },
    async upload() {
      this.progress = 0;
      this.currentFile = this.$refs.file.files.item(0);
      const formData = new FormData();
      formData.append('file', this.currentFile, `${this.currentFile.name}`);
      this.showFileOnServer = true;
      this.progress = 0;
      try {
        const res = await apiClient.post(
          '/dynamicforms/preupload-file/',
          formData,
          {
            showProgress: false,
            onUploadProgress: function onUploadProgress(progressEvent) {
              if (!progressEvent.computable) {
                this.progress = 50;
              } else {
                this.progress = Math.round((progressEvent.loaded * 100) / progressEvent.total);
              }
            },
          },
        );
        this.value = res.data.identifier;
        this.progress = 100;
      } catch (err) {
        this.progress = 0;
        this.showFileOnServer = false;
        this.currentFile = undefined;
        this.fileInputKey = Math.round(Math.random() * 1000);
        throw err;
      }
    },
  },
};
</script>
