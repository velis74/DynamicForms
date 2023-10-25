<template>
  <v-checkbox
    v-model="boolValue"
    :indeterminate="indeterminate"
    :false-value="false"
    :true-value="true"
    :class="field.renderParams.fieldCSSClass"
    :name="field.name"
    :readonly="field.readOnly"
    :disabled="field.readOnly"
    v-bind="baseBinds"
    @change="change"
  />
</template>

<script setup lang="ts">

import {BaseEmits, BaseProps, useInputBase} from "./base-composable";
import {computed, onMounted, ref} from "vue";
import _ from "lodash";

interface Props extends BaseProps {}
const props = defineProps<Props>();

interface Emits extends BaseEmits {}
const emits = defineEmits<Emits>();

const {value} = useInputBase(props, emits);

//data //internalValue: false as boolean | null
let internalValue = ref<boolean | null >(false);

//computed
const indeterminate = computed(() => {
  return props.field.allowNull && (internalValue.value == null);
})


const boolValue = computed({
  get(): any{
    return internalValue.value;
  },
  set(newVal: boolean)
  {
    console.log(value.value, newVal);
  },
})

//mounted
onMounted(() => {
  if (value.value) {
    internalValue.value = true;
  } else if (props.field.allowNull && value.value == null) {
    internalValue.value = null;
  } else {
    internalValue.value = false;
  }
})

//methods
function  change() {
  const oldVal = _.clone(internalValue.value);
  if (oldVal === true) {
    internalValue.value = props.field.allowNull ? null : false;
  } else {
    internalValue.value = oldVal === false;
  }
  value.value = internalValue.value;
}




</script>

<script lang="ts">

import { defineComponent } from 'vue';

import TranslationsMixin from '../../util/translations-mixin';

export default /* #__PURE__ */ defineComponent({
    mixins: [TranslationsMixin],

});

</script>
