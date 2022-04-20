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
import Form from './form';
import FormLayout from './layout_vuetify';

export default {
  name: 'VuetifyForm',
  components: { FormLayout },
  mixins: [Form],
  methods: {
    valueChanged(payload) {
      console.log('a', payload);
    },
  },
};
</script>
