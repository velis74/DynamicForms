<template>
  <b-card>
    <template #header>
      {{ title }}
      <v-layout v-if="actions.formHeader().length" justify-end>
        <df-actions :actions="actions.formHeader()"/>
      </v-layout>
    </template>
    <b-card-text>
      <FormLayout :is="layout.componentName" :layout="layout" :payload="payload" :actions="actions"/>
    </b-card-text>
    <template #footer>
      <b-row class="text-right">
        <b-col>
          <df-actions :actions="actions.formFooter()"/>
        </b-col>
      </b-row>
    </template>
  </b-card>
</template>

<script>
import { DfActions } from '../public';

import Form from './form';
import FormLayout from './layout';

export default {
  name: 'BootstrapForm',
  components: { FormLayout, DfActions },
  mixins: [Form],
};
</script>
