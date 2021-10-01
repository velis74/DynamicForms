<template>
  <DFWidgetBase :def="def" :data="data" :errors="errors" :show-label-or-help-text="showLabelOrHelpText">
    <div
      :id="def.uuid"
      slot="input"
      :key="def.uuid"
    >
      <div class="input-group">
        <input
          ref="file"
          :key="fileInputKey"
          type="file"
          :readonly="def.read_only === true"
          :disabled="def.read_only === true"
          :name="def.name"
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
            {{ getFileName(currentFile ? currentFile.name : data[def.name]) }}
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
    </div>
  </DFWidgetBase>
</template>

<script>
import _ from 'lodash';

import DFWidgetBase from './dfwidgetbase.vue';

import apiClient from '@/apiClient';
import helperFunctions from '@/logic/helperFunctions';

export default {
  name: 'DFWidgetFile',
  components: { DFWidgetBase },
  props: {
    def: { type: Object, required: true },
    data: { type: Object, required: true },
    errors: { type: Object, required: true },
    showLabelOrHelpText: { type: Boolean, default: true },
  },
  data() {
    return {
      currentFile: undefined,
      progress: 0,
      showFileOnServer: false,
      fileInputKey: Math.round(Math.random() * 1000),
    };
  },
  mounted() {
    this.showFileOnServer = !!_.clone(this.data[this.def.name]);
  },
  methods: {
    getFileName(val) {
      return helperFunctions.getFileNameFromPath(val);
    },
    selectFile() {
      this.upload();
    },
    removeFile() {
      this.data[this.def.name] = null;  // eslint-disable-line
      this.progress = 0;
      this.fileInputKey = Math.round(Math.random() * 1000);
      this.showFileOnServer = false;
      this.currentFile = undefined;
    },
    upload() {
      this.progress = 0;
      this.currentFile = this.$refs.file.files.item(0);

      const formData = new FormData();
      formData.append('file', this.currentFile, `${this.currentFile.name}`);

      this.showFileOnServer = true;

      this.progress = 0;
      this.progress = 45;
      // make this better, some timeout repeating function
      this.progress = 60;
      apiClient.post('/dynamicforms/preupload-file/', formData, { showProgress: false }).then((res) => {
        this.data[this.def.name] = res.data.identifier;  // eslint-disable-line
        this.progress = 100;
      }).catch((err) => {
        this.progress = 0;
        this.currentFile = undefined;
        console.error(err);
      });
    },
  },
};
</script>
