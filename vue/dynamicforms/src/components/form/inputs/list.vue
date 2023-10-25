<template>
  <v-input v-bind="binds">
    <APIConsumerVue v-if="consumer" :consumer="consumer" :display-component="displayComponent"/>
  </v-input>
</template>

<script setup lang="ts">
import {BaseEmits, BaseProps, useInputBase} from "./base-composable";
import {computed, onBeforeMount, onMounted, ref, watch} from "vue";
import _ from "lodash";
import {APIConsumer} from "../../api_consumer/namespace";
import ComponentDisplay from "../../api_consumer/component-display";
import ConsumerLogicArray from "../../api_consumer/consumer-logic-array";


interface Props extends BaseProps {}
const props = defineProps<Props>();

interface Emits extends BaseEmits {}
const emits = defineEmits<Emits>();

const {baseBinds} = useInputBase(props, emits);

//computed
const binds = computed(() => {
  const binds = _.cloneDeep(baseBinds);
  binds.value['error-messages'] = binds.value['error-messages']
    .filter((el: any) => !(el === undefined || el === null || !Object.keys(el).length))
    .map((el: { [key: string]: string }) => Object.keys(el).map((key) => `${key}: ${el[key]}`));
    return binds;
})

//setup()
const consumer = ref<APIConsumer.ConsumerLogicBaseInterface | undefined>();
const displayComponent = ComponentDisplay.TABLE;
async function setConsumer(definition: DfForm.FormComponentDefinition, modelValue: any[]) {
  consumer.value = new ConsumerLogicArray(definition, modelValue);
  await consumer.value?.reload();
}


//mounted & before mount
onBeforeMount(() => {
 if (props.modelValue == null) {
    // when creating new records we might get undefined, this breaks the reactivity
    // update value with an empty array of records to avoid further complications
    emits('update:modelValue', []);
  }
});

//this one should be async
onMounted(async() => {
  // `${this.field.renderParams.formComponentDef?.detail_url.split('/').slice(0, -1).join('/')}.componentdef`,
  await setConsumer(
    props.field.renderParams.formComponentDef!,
    props.modelValue as any[],
  );
});

//watch
watch(props.modelValue, (newValue: any) => {
  consumer.value = new ConsumerLogicArray(props.field.renderParams.formComponentDef!, newValue);
})



</script>

<script lang="ts">

import { defineComponent } from 'vue';


import TranslationsMixin from '../../util/translations-mixin';
import { DfForm } from '../namespace';

import InputBase from './base';

export default defineComponent({

  mixins: [TranslationsMixin],





});
</script>
