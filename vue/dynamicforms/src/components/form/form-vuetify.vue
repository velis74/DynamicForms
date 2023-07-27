<template>
  <v-card>
    <v-card-title>
      {{ title }}
      <v-layout v-if="actions.formHeader.length" justify-end>
        <df-actions :actions="actions.formHeader"/>
      </v-layout>
    </v-card-title>
    <v-card-text>
      <FormLayout :is="layout.componentName" :layout="layout" :payload="payload" :actions="actions" :errors="errors"/>
    </v-card-text>
    <v-card-actions class="vuetify-form-actions">
      <v-layout justify-end>
        <df-actions :actions="actions.formFooter"/>
      </v-layout>
    </v-card-actions>
  </v-card>
</template>

<script lang="ts">
import { computed, defineComponent } from 'vue';

import Form from './form';
import FormLayout from './layout-vuetify.vue';

export default /* #__PURE__ */ defineComponent({
  name: 'VuetifyForm',
  components: { FormLayout },
  mixins: [Form],
  provide() {
    return { payload: computed(() => this.payload) };
  },
});
</script>

<style>
  .vuetify-form-actions {
    margin-right: 1em;
  }
</style>
