<template>
  <div class="field-clear-icon" @click="clear">
    <IonIcon name="trash-outline"/>
  </div>
</template>

<script setup lang="ts">
import {BaseEmits, BaseProps, useInputBase} from "./base-composable";
import IonIcon from 'vue-ionicon';

interface Emits {
  (e: 'clearButtonPressed', value: any): any
}
const emits = defineEmits<Emits>();


//methods
function clear() {
  emits('clearButtonPressed', null);
}

</script>

