<script setup lang="ts">
import { computed, provide } from 'vue';
import { useDisplay } from 'vuetify';

import FilteredActions from '../actions/filtered-actions';
import { APIConsumer } from '../api_consumer/namespace';

import FormPayload from './definitions/form-payload';
import FormLayoutClass from './definitions/layout';
import FormLayout from './layout-vuetify.vue';

interface Props {
  title: string
  pkName: string
  pkValue: APIConsumer.PKValueType
  layout: FormLayoutClass
  payload: FormPayload
  actions: FilteredActions
  errors: any
}

const props = defineProps<Props>();
const useDisplayInstance = useDisplay();

provide('payload', computed(() => props.payload));
</script>

<template>
  <v-card>
    <v-card-title>
      {{ title }}
      <v-layout v-if="actions.formHeader.length" justify-end>
        <df-actions :actions="actions.formHeader" :use-display="useDisplayInstance"/>
      </v-layout>
    </v-card-title>
    <v-card-text>
      <FormLayout :is="layout.componentName" :layout="layout" :payload="payload" :actions="actions" :errors="errors"/>
    </v-card-text>
    <v-card-actions class="vuetify-form-actions">
      <v-layout justify-end>
        <df-actions :actions="actions.formFooter" :use-display="useDisplayInstance"/>
      </v-layout>
    </v-card-actions>
  </v-card>
</template>

<style>
  .vuetify-form-actions {
    margin-right: 1em;
  }
</style>
