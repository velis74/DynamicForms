<template>
  <df-file
    v-model="value"
    :comms="fileComms"
    :class="field.renderParams.fieldCSSClass"
    :name="field.name"
    :errors="baseBinds['error-messages']"
    :enabled="!field.readOnly"
    :hint="baseBinds.hint"
    v-bind="baseBinds"
  />
</template>

<script setup lang="ts">
import { DfFile, FileComms } from '@dynamicforms/vuetify-inputs';

import { BaseEmits, BaseProps, useInputBase } from './base';

import { apiClient } from '@/util';

interface Props extends BaseProps { }
const props = defineProps<Props>();

interface Emits extends BaseEmits { }
const emits = defineEmits<Emits>();

const { value, baseBinds } = useInputBase(props, emits);

const fileComms: FileComms = {
  upload: async (file, progressCallback) => {
    const formData = new FormData();
    formData.append('file', file, file.name);

    const res = await apiClient.post(
      '/dynamicforms/preupload-file/',
      formData,
      {
        showProgress: false,
        onUploadProgress: function onUploadProgress(progressEvent) {
          if (progressEvent.event.lengthComputable && progressCallback != null) {
            progressCallback(progressEvent.loaded, progressEvent.total ?? 0);
          }
        },
      },
    );
    console.log(res.data.identifier);
    return res.data.identifier;
  },

  delete: async (fileIdentifier) => {
    await apiClient.delete(`/dynamicforms/preupload-file/${encodeURIComponent(fileIdentifier)}/`);
    // In a real implementation, this would call an API to delete the file
    // console.log('Deleting file:', fileIdentifier);

    return Promise.resolve();
  },

  touch: async (fileIdentifier) => {
    // In a real implementation, this would call an API to "touch" the file
    console.log('Touching file:', fileIdentifier);
    return Promise.resolve();
  },
};
</script>
