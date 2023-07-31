<template>
  <div v-if="errorText">{{ errorText }}</div>
  <APIConsumerVue v-else-if="consumer" :consumer="consumer" :display-component="displayComponent"/>
  <div v-else/>
</template>

<script setup lang="ts">
import { onMounted, ref, Ref, watch } from 'vue';
import { RouteLocationNormalized, useRoute } from 'vue-router';

import APIConsumerVue from './api-consumer.vue';
import ComponentDisplay from './component-display';
import ConsumerLogicApi from './consumer-logic-api';
import { APIConsumer } from './namespace';

const consumer = ref<APIConsumer.ConsumerLogicBaseInterface | undefined>();
// test: undefined as FormLayout | undefined,
const errorText: Ref<string | undefined> = ref();
const displayComponent = ref(ComponentDisplay.TABLE);

const route = useRoute();
const emit = defineEmits(['title-change', 'load-route']);

async function goToRoute(to: RouteLocationNormalized) {
  if (!(<string>to.name).startsWith('CL ')) return;
  const consumerTemp = new ConsumerLogicApi(to.path);
  try {
    await consumerTemp.getFullDefinition();
    errorText.value = undefined;
    consumer.value = consumerTemp;
    emit('title-change', consumer.value.title(displayComponent.value === ComponentDisplay.TABLE ? 'table' : 'new'));
  } catch (err: any) {
    console.error(err);
    errorText.value = err.toString();
  }
}

onMounted(() => { goToRoute(route); });
watch(() => route.path, () => goToRoute(route));
</script>
