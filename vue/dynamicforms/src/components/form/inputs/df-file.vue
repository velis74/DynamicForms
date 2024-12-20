<template>
  <vuetify-input
    :label="baseBinds.label"
    :messages="[...baseBinds.messages, modelValue]"
    :error-messages="baseBinds['error-messages']"
    :error-count="baseBinds['error-count']"
  >
    <div style="position: relative; width: 100%">
      <v-progress-linear
        v-if="currentFile && progress < 100"
        :model-value="progress"
        :indeterminate="progress === -1"
        height="10"
        style="position: absolute; top: 50%; transform: translateY(-50%); width: 100%;"
      />
      <v-file-input
        v-model="selectedFile"
        :readonly="field.readOnly"
        :disabled="field.readOnly"
        :name="field.name"
        :label="baseBinds.label"
        :show-size="true"
        :multiple="false"
        clearable
        :style="currentFile && progress < 100 ? 'visibility: hidden' : ''"
        @update:model-value="handleFileChange"
        @click:clear="removeFile"
      />
    </div>
  </vuetify-input>
</template>

<script setup lang="ts">
import { ref } from 'vue';

import apiClient from '../../util/api-client';

import { BaseEmits, BaseProps, useInputBase } from './base';
import VuetifyInput from './input-vuetify.vue';

interface Props extends BaseProps {}

const props = defineProps<Props>();

interface Emits extends BaseEmits {}

const emits = defineEmits<Emits>();

const { value, baseBinds } = useInputBase(props, emits);

// State
const currentFile = ref<File | null>(null);
const progress = ref(0);
const fileInputKey = ref(Math.round(Math.random() * 1000));
const selectedFile = ref<File | null>();

async function removeFile() {
  if (value.value) {
    try {
      await apiClient.delete(`/dynamicforms/preupload-file/${value.value}/`);
    } catch (err) {
      console.error('Napaka pri brisanju datoteke:', err);
      // Ne vrže napake, ker datoteka tako ali tako ni več prikazana
    }
  }

  value.value = null;
  progress.value = 0;
  fileInputKey.value = Math.round(Math.random() * 1000);
  currentFile.value = null;
  selectedFile.value = null;
}

async function upload(file: File) {
  console.log('upload received file:', file);
  progress.value = -1;
  currentFile.value = file;

  const formData = new FormData();
  formData.append('file', file, file.name);
  console.log('formData:', formData);

  try {
    const res = await apiClient.post(
      '/dynamicforms/preupload-file/',
      formData,
      {
        showProgress: false,
        onUploadProgress: function onUploadProgress(progressEvent) {
          if (progressEvent.event.lengthComputable) {
            progress.value = Math.round((progressEvent.loaded * 100) / <number> progressEvent.total);
          }
        },
      },
    );
    value.value = res.data.identifier;
    progress.value = 100;
  } catch (err) {
    progress.value = 0;
    currentFile.value = null;
    fileInputKey.value = Math.round(Math.random() * 1000);
    selectedFile.value = null;
    throw err;
  }
}

function handleFileChange(file: File | File[]): any {
  console.log('handleFileChange file:', file);
  if (file) {
    if (Array.isArray(file)) {
      console.error('Uploading multiple files not supported right now');
    } else {
      console.log('calling upload with file:', file);
      upload(file);
    }
  }
}
</script>
