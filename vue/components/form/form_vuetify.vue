<template>
  <v-card>
    <v-card-title>{{ title }}<!--TODO: actions--></v-card-title>
    <v-card-text>
      <FormLayout :is="layout.componentName" :layout="layout" :payload="payload" @value-changed="valueChanged"/>
    </v-card-text>
    <v-card-actions>
      <!--TODO: actions-->
    </v-card-actions>
  </v-card>
</template>

<script>
import FormPayload from './definitions/form_payload';
import FormLayoutClass from './definitions/layout';
import FormLayout from './layout_vuetify';

export default {
  name: 'VuetifyForm',
  components: { FormLayout },
  props: {
    pkName: { type: String, required: true },
    title: { type: String, required: true },
    pkValue: { type: null, required: true },
    layout: { type: FormLayoutClass, required: true },
    payload: { type: FormPayload, required: true },
  },
  data() { return {}; },
  computed: {},
  methods: {
    valueChanged(payload) {
      console.log('a', payload);
    },
  },
};
</script>
