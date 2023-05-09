<template>
  <div v-if="errorText">{{ errorText }}</div>
  <APIConsumerVue v-else-if="consumer" :consumer="consumer" :display-component="displayComponent"/>
  <div v-else/>
</template>

<script lang="ts">
import { defineComponent } from 'vue';

import FormLayout from '../form/definitions/layout';

import APIConsumerVue from './api-consumer.vue';
import ComponentDisplay from './component-display';
import ConsumerLogicApi from './consumer-logic-api';
import { APIConsumer } from './namespace';

export default defineComponent({
  name: 'APIConsumerLoader',
  components: { APIConsumerVue },
  emits: ['title-change', 'load-route'],
  data() {
    return {
      consumer: undefined as APIConsumer.ConsumerLogicAPIInterface | undefined,
      test: undefined as FormLayout | undefined,
      errorText: undefined as string | undefined,
      displayComponent: ComponentDisplay.TABLE,
    };
  },
  watch: { $route(to) { this.goToRoute(to); } },
  mounted() { this.goToRoute(this.$route); },
  methods: {
    async goToRoute(to: any) {
      if (!to.name.startsWith('CL ')) return;
      const consumer = new ConsumerLogicApi(to.path);
      try {
        await consumer.getFullDefinition();
        this.errorText = undefined;
        this.consumer = consumer;
        this.$emit('title-change', consumer.title(this.displayComponent === ComponentDisplay.TABLE ? 'table' : 'new'));
      } catch (err: any) {
        console.error(err);
        this.errorText = err.toString();
      }
    },
  },
});
</script>
