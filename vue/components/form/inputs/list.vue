<template>
  <APIConsumer v-if="consumer" :consumer="consumer" :display-component="displayComponent"/>
</template>

<script lang="ts">
import { defineComponent } from 'vue';

import APIConsumerLogic from '../../api_consumer/api-consumer-logic';
import APIConsumer from '../../api_consumer/api-consumer.vue';
import ComponentDisplay from '../../api_consumer/component-display';
import TranslationsMixin from '../../util/translations-mixin';

import InputBase from './base';

export default defineComponent({
  name: 'DList',
  components: { APIConsumer },
  mixins: [InputBase, TranslationsMixin],
  data() {
    return { consumer: null as APIConsumerLogic | null };
  },
  computed: {
    displayComponent() {
      return ComponentDisplay.TABLE;
    },
  },
  mounted() {
    this.consumer = new APIConsumerLogic(
      `${this.field.renderParams.formComponentDef?.detail_url.split('/').slice(0, -1).join('/')}`,
    );
    this.consumer.filter({ event: 1 });
    this.consumer.getFullDefinition();
  },
});
</script>

<style scoped>

</style>
