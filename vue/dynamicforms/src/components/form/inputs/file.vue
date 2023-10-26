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

<script setup lang="ts">
/**
 * TODO: the field has a different mechanism for clearing than e.g. datetime: this one's using x while the other
 *   is using IonIcon
 */
import _ from 'lodash';
import { onMounted, ref } from 'vue';

import apiClient from '../../util/api-client';

import { BaseEmits, BaseProps, useInputBase } from './base-composable';
import InputClearButton from './clear-input-button.vue';
import VuetifyInput from './input-vuetify.vue';

interface Props extends BaseProps {}
const props = defineProps<Props>();

interface Emits extends BaseEmits {}
const emits = defineEmits<Emits>();

const { value, baseBinds } = useInputBase(props, emits);

// data
// currentFile: null as (File | null)
let currentFile: File | null = null;
// progress: 0,
let progress = 0;
// showFileOnServer: false,
let showFileOnServer = false;
// fileInputKey: Math.round(Math.random() * 1000),
let fileInputKey = Math.round(Math.random() * 1000);

const file = ref<HTMLInputElement>();

// mounted
onMounted(() => {
  showFileOnServer = !!_.clone(value.value);
});

// methods
function getFileName(filePath: string) {
  // returns just the filename without any path
  return !filePath ? filePath : filePath.replace(/^.*[\\/]/, '');
}

function removeFile() {
  value.value = null;  // eslint-disable-line
  progress = 0;
  fileInputKey = Math.round(Math.random() * 1000);
  showFileOnServer = false;
  currentFile = null;
}

async function upload() {
  progress = 0;
  const fileRef = file.value!;
  if (!fileRef || !fileRef.files) return;
  currentFile = fileRef.files.item(0);
  const formData = new FormData();
  formData.append('file', currentFile as File, `${(<File> currentFile).name}`);
  showFileOnServer = true;
  progress = 0;
  try {
    const res = await apiClient.post(
      '/dynamicforms/preupload-file/',
      formData,
      {
        showProgress: false,
        onUploadProgress: function onUploadProgress(progressEvent) {
          if (!progressEvent.event.lengthComputable) {
            progress = 50;
          } else {
            progress = Math.round((progressEvent.loaded * 100) / <number> progressEvent.total);
          }
        },
      },
    );
    value.value = res.data.identifier;
    progress = 100;
  } catch (err) {
    progress = 0;
    showFileOnServer = false;
    currentFile = null;
    fileInputKey = Math.round(Math.random() * 1000);
    throw err;
  }
}

function selectFile() {
  upload();
}

</script>
