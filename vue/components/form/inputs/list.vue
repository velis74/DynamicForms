<template>
  <APIConsumer v-if="consumer" :consumer="consumer" :display-component="displayComponent"/>
</template>

<script lang="ts">
import { defineComponent } from 'vue';

import APIConsumer from '../../api_consumer/api-consumer.vue';
import ComponentDisplay from '../../api_consumer/component-display';
import ConsumerLogic from '../../api_consumer/consumer-logic';
import apiClient from '../../util/api-client';
import TranslationsMixin from '../../util/translations-mixin';

import InputBase from './base';

export default defineComponent({
  name: 'DList',
  components: { APIConsumer },
  mixins: [InputBase, TranslationsMixin],
  data() {
    return { consumer: null as ConsumerLogic | null };
  },
  computed: {
    displayComponent() {
      return ComponentDisplay.TABLE;
    },
  },
  beforeMount() {
    if (this.modelValue == null) {
      // when creating new records we might get undefined, this breaks the reactivity
      // update value with an empty array of records to avoid further complications
      this.$emit('update:modelValue', []);
    }
  },
  async mounted() {
    const definition = (await apiClient.get(
      `${this.field.renderParams.formComponentDef?.detail_url.split('/').slice(0, -1).join('/')}.componentdef`,
    )).data;
    this.consumer = new ConsumerLogic(definition, this.modelValue as any[]);
  },
});
</script>

<style scoped>

</style>
