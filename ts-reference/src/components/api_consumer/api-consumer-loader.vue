<template>
  <div v-if="errorText">{{ errorText }}</div>
  <APIConsumer v-else-if="consumer" :consumer="consumer" :display-component="displayComponent"/>
  <div v-else/>
</template>

<script lang="ts">
import { defineComponent } from 'vue';

import APIConsumer from './api-consumer.vue';
import APIConsumerLogic from './api-consumer-logic';
import ComponentDisplay from './component-display';

export default defineComponent({
  name: 'APIConsumerLoader',
  components: { APIConsumer },
  emits: ['title-change', 'load-route'],
  data() {
    return {
      consumer: null as any,
      errorText: null as any,
      displayComponent: ComponentDisplay.TABLE,
    };
  },
  watch: { $route(to) { this.goToRoute(to); } },
  mounted() { this.goToRoute(this.$route); },
  methods: {
    async goToRoute(to: any) {
      const consumer = new APIConsumerLogic(to.path);
      try {
        await consumer.getFullDefinition();
        this.errorText = null;
        this.consumer = consumer;
        this.$emit('title-change', consumer.title(this.displayComponent === ComponentDisplay.TABLE ? 'table' : 'new'));
      } catch (err: any) {
        this.errorText = err.toString();
      }
    },
  },
});
</script>
