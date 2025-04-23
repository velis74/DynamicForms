<template>
  <v-input v-bind="binds">
    <APIConsumerVue
      v-if="consumer"
      :consumer="consumer"
      :display-component="displayComponent"
      :handlers="handlers"
      :dialog-handlers="dialogHandlers"
    />
  </v-input>
</template>

<script setup lang="ts">
import { cloneDeep } from 'lodash-es';
import { computed, onBeforeMount, onMounted, ref, watch } from 'vue';

import APIConsumerVue from '../../api_consumer/api-consumer.vue';
import ComponentDisplay from '../../api_consumer/component-display';
import ConsumerLogicArray from '../../api_consumer/consumer-logic-array';
import { APIConsumer } from '../../api_consumer/namespace';
import { DfForm } from '../namespace';

import { BaseEmits, BaseProps, useInputBase } from './base';

interface Props extends BaseProps {}
const props = defineProps<Props>();

interface Emits extends BaseEmits {}
const emits = defineEmits<Emits>();

const { baseBinds } = useInputBase(props, emits);

// computed
const binds = computed(() => {
  const bindsClone = cloneDeep(baseBinds);
  bindsClone.value['error-messages'] = bindsClone.value['error-messages']
    .filter((el: any) => !(el === undefined || el === null || !Object.keys(el).length))
    .map((el: { [key: string]: string }) => Object.keys(el).map((key) => `${key}: ${el[key]}`));
  return bindsClone;
});

// setup()
const consumer = ref<APIConsumer.ConsumerLogicBaseInterface | undefined>();
const displayComponent = ComponentDisplay.TABLE;
async function setConsumer(definition: DfForm.FormComponentDefinition, modelValue: any[]) {
  consumer.value = new ConsumerLogicArray(definition, modelValue);
  await consumer.value?.reload();
}

// mounted & before mount
onBeforeMount(() => {
  if (props.modelValue == null) {
    // when creating new records we might get undefined, this breaks the reactivity
    // update value with an empty array of records to avoid further complications
    emits('update:modelValue', []);
  }
});

onMounted(async () => {
  // `${this.field.renderParams.formComponentDef?.detail_url.split('/').slice(0, -1).join('/')}.componentdef`,
  await setConsumer(
    props.field.renderParams.formComponentDef!,
    props.modelValue as any[],
  );
});

// watch
watch(props.modelValue, async (newValue: any) => {
  await setConsumer(props.field.renderParams.formComponentDef!, newValue);
});

</script>
