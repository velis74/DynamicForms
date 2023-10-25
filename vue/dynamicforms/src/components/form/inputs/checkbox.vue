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
import _ from 'lodash';
import { computed, onMounted, ref } from 'vue';

import { BaseEmits, BaseProps, useInputBase } from './base-composable';

interface Props extends BaseProps {}
const props = defineProps<Props>();

interface Emits extends BaseEmits {}
const emits = defineEmits<Emits>();

const { value, baseBinds } = useInputBase(props, emits);

// data
const internalValue = ref<boolean | null >(false);

// computed
const indeterminate = computed(() => props.field.allowNull && (internalValue.value == null));

const boolValue = computed({
  get(): any {
    return internalValue.value;
  },
  set(newVal: boolean) {
    console.log(value.value, newVal);
  },
});

// mounted
onMounted(() => {
  if (value.value) {
    internalValue.value = true;
  } else if (props.field.allowNull && value.value == null) {
    internalValue.value = null;
  } else {
    internalValue.value = false;
  }
});

// methods
function change() {
  const oldVal = _.clone(internalValue.value);
  if (oldVal === true) {
    internalValue.value = props.field.allowNull ? null : false;
  } else {
    internalValue.value = oldVal === false;
  }
  value.value = internalValue.value;
}

</script>
