<template>
  <vuetify-input
    :label="baseBinds.label"
    :messages="baseBinds.messages"
    :error-messages="baseBinds['error-messages']"
    :error-count="baseBinds['error-count']"
  >
    <div style="width: 100%;">
      <v-textarea
        :id="field.uuid"
        v-model="value"
        :type="inputType"
        variant="underlined"
        :class="field.renderParams.fieldCSSClass"
        :name="field.name"
        :placeholder="field.placeholder"

        :minlength="minLength"
        :maxlength="maxLength"
        :step="field.renderParams.step"
        :size="field.renderParams.size"

        :readonly="field.readOnly"
        :disabled="field.readOnly"
      />
    </div>
  </vuetify-input>
</template>

<script setup lang="ts">

import {BaseEmits, BaseProps, useInputBase} from "./base-composable";
import {computed} from "vue";
import VuetifyInput from './input-vuetify.vue';

interface Props extends BaseProps {}
const props = defineProps<Props>();

interface Emits extends BaseEmits {}
const emits = defineEmits<Emits>();

const {baseBinds} = useInputBase(props, emits);

//computed
const inputType = computed(() => {
  return props.field.renderParams.inputType;
})

const minLength = computed(() => {
  return props.field.renderParams.minLength;
})

const  maxLength = computed(() => {
  return props.field.renderParams.maxLength;
})


const value = computed({
  get(): any{
   return props.modelValue;
  },
  set(newVal: string)
  {
    emits('update:modelValue', newVal);
  },
})


</script>

<script lang="ts">
import { defineComponent } from 'vue';

import TranslationsMixin from '../../util/translations-mixin';

export default /* #__PURE__ */ defineComponent({
  mixins: [TranslationsMixin],

});
</script>
