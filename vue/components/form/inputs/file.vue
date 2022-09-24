<template>
  <vuetify-input
    :label="baseBinds.label"
    :messages="baseBinds.messages"
    :error-messages="baseBinds['error-messages']"
    :error-count="baseBinds['error-count']"
  >
    <div>
      <div>
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
        <v-progress-linear v-if="currentFile" :value="progress" height="10" style="margin-top: 5px;"/>
        <div>
          <div v-if="showFileOnServer" style="display: inline-block;">
            <p>
              {{ getFileName(currentFile ? currentFile.name : value) }}
              <InputClearButton style="float: right; width: 1rem; margin-top: .1rem;" @clearButtonPressed="removeFile"/>
            </p>
          </div>
        </div>
      </div>
    </div>
  </vuetify-input>
</template>

<script>
/**
 * TODO: the field has a different mechanism for clearing than e.g. datetime: this one's using x while the other
 *   is using IonIcon
 */
import _ from 'lodash';

import apiClient from '../../util/api-client';
import TranslationsMixin from '../../util/translations-mixin';

import InputBase from './base';
import InputClearButton from './clear-input-button';
import VuetifyInput from './input-vuetify';

export default {
  name: 'DFile',
  components: { VuetifyInput, InputClearButton },
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
