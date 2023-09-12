<template>
  <v-input v-bind="binds">
    <APIConsumerVue v-if="consumer" :consumer="consumer" :display-component="displayComponent"/>
  </v-input>
</template>

<script lang="ts">
import _ from 'lodash';
import { defineComponent, ref } from 'vue';

import APIConsumerVue from '../../api_consumer/api-consumer.vue';
import ComponentDisplay from '../../api_consumer/component-display';
import ConsumerLogicArray from '../../api_consumer/consumer-logic-array';
import { APIConsumer } from '../../api_consumer/namespace';
import TranslationsMixin from '../../util/translations-mixin';
import { DfForm } from '../namespace';

import InputBase from './base';

export default defineComponent({
  name: 'DList',
  components: { APIConsumerVue },
  mixins: [InputBase, TranslationsMixin],
  setup() {
    const consumer = ref<APIConsumer.ConsumerLogicBaseInterface | undefined>();
    const displayComponent = ComponentDisplay.TABLE;

    async function setConsumer(definition: DfForm.FormComponentDefinition, modelValue: any[]) {
      consumer.value = new ConsumerLogicArray(definition, modelValue);
    }
    return { displayComponent, setConsumer, consumer };
  },
  computed: {
    binds() {
      const binds = _.cloneDeep(this.baseBinds);
      binds['error-messages'] = binds['error-messages']
        .filter((el: any) => !(el === undefined || el === null || !Object.keys(el).length))
        .map((el: { [key: string]: string }) => Object.keys(el).map((key) => `${key}: ${el[key]}`));
      return binds;
    },
  },
  watch: {
    modelValue(newValue) {
      this.consumer = new ConsumerLogicArray(this.field.renderParams.formComponentDef!, newValue);
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
    // `${this.field.renderParams.formComponentDef?.detail_url.split('/').slice(0, -1).join('/')}.componentdef`,
    await this.setConsumer(
      this.field.renderParams.formComponentDef!,
      this.modelValue as any[],
    );
  },
});
</script>
