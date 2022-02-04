<template>
  <div v-if="errorText">{{ errorText }}</div>
  <APIConsumer v-else-if="consumer" :consumer="consumer" :display-component="displayComponent"/>
  <div v-else/>
</template>

<script>
import APIConsumer from './api_consumer';
import APIConsumerLogic from './api_consumer_logic';
import ComponentDisplay from './component_display';

export default {
  name: 'APIConsumerLoader',
  components: { APIConsumer },
  emits: ['title-change', 'load-route'],
  data() {
    return {
      consumer: null,
      errorText: null,
      displayComponent: ComponentDisplay.TABLE,
    };
  },
  watch: { $route(to) { this.goToRoute(to); } },
  mounted() { this.goToRoute(this.$route); },
  methods: {
    async goToRoute(to) {
      const consumer = new APIConsumerLogic(to.path);
      try {
        await consumer.getFullDefinition();
        this.errorText = null;
        this.consumer = consumer;
        this.$emit('title-change', consumer.title(this.displayComponent === ComponentDisplay.TABLE ? 'table' : 'new'));
      } catch (err) {
        console.error(err);
        this.errorText = err.toString();
      }
    },
  },
};
</script>
