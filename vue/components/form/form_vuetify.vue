<template>
  <v-card>
    <v-card-title>
      {{ title }} ssss
      <v-layout v-if="actions.formHeader().length" justify-end>
        <df-actions :actions="actions.formHeader()"/>
      </v-layout>
    </v-card-title>
    <v-card-text>
      <FormLayout :is="layout.componentName" :layout="layout" :payload="payload" :actions="actions"/>
    </v-card-text>
    <v-card-actions class="vuetify-form-actions">
      <v-layout justify-end>
        <df-actions :actions="actions.formFooter()"/>
      </v-layout>
    </v-card-actions>
  </v-card>
</template>

<script>
import { DfActions } from '../public';

import Form from './form';
import FormLayout from './layout';

export default {
  name: 'VuetifyForm',
  components: { FormLayout, DfActions },
  mixins: [Form],
};
</script>

<style>
  .vuetify-form-actions {
    margin-right: 1em;
  }
</style>
