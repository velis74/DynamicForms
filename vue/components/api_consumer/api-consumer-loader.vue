<template>
  <div v-if="errorText">{{ errorText }}</div>
  <APIConsumer v-else-if="consumer" :consumer="consumer" :display-component="displayComponent"/>
  <div v-else/>
</template>

<script lang="ts">
import { defineComponent } from 'vue';

import APIConsumerLogic from './api-consumer-logic';
import APIConsumer from './api-consumer.vue';
import ComponentDisplay from './component-display';

export default defineComponent({
  name: 'APIConsumerLoader',
  components: { APIConsumer },
  emits: ['title-change', 'load-route'],
  data() {
    return {
      consumer: null as APIConsumerLogic | null,
      errorText: null,
      displayComponent: ComponentDisplay.TABLE,
    };
  },
  watch: { $route(to) { this.goToRoute(to); } },
  mounted() { this.goToRoute(this.$route); },
  methods: {
    async goToRoute(to: any) {
      if (!to.name.startsWith('CL ')) return;
      const consumer = new APIConsumerLogic(to.path);
      try {
        await consumer.getFullDefinition();
        this.errorText = null;
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
