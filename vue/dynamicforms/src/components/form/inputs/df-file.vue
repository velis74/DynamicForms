<template>
  <vuetify-input
    :label="baseBinds.label"
    :error-messages="baseBinds['error-messages']"
    :error-count="baseBinds['error-count']"
    :hint="baseBinds.hint"
    :persistent-hint="baseBinds['persistent-hint']"
    :hide-details="baseBinds['hide-details']"
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
        :label="fileLabel"
        :readonly="field.readOnly"
        :disabled="field.readOnly"
        :name="field.name"
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
import { ref, computed } from 'vue';

import { BaseEmits, BaseProps, useInputBase } from './base';
import VuetifyInput from './input-vuetify.vue';

import { apiClient } from '@/util';

interface Props extends BaseProps {
}

const props = defineProps<Props>();

interface Emits extends BaseEmits {
}

const emits = defineEmits<Emits>();

const { value, baseBinds } = useInputBase(props, emits);

// State
const currentFile = ref<File | null>(null);
const progress = ref(0);
const fileInputKey = ref(Math.round(Math.random() * 1000));
const selectedFile = ref<File | null>();

const fileLabel = computed(() => {
  if (!selectedFile.value && value.value) {
    return props.modelValue;
  }
  return '';
});

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
  progress.value = -1;
  currentFile.value = file;

  const formData = new FormData();
  formData.append('file', file, file.name);

  try {
    const res = await apiClient.post(
      '/dynamicforms/preupload-file/',
      formData,
      {
        showProgress: false,
        onUploadProgress: function onUploadProgress(progressEvent) {
          if (progressEvent.event.lengthComputable) {
            progress.value = Math.round((progressEvent.loaded * 100) / <number>progressEvent.total);
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
  if (file) {
    if (Array.isArray(file)) {
      console.error('Uploading multiple files not supported right now');
    } else {
      upload(file);
    }
  }
}
</script>
