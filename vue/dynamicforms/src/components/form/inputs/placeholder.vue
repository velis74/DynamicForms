<template>
  <v-input v-bind="baseBinds">
    <v-alert type="warning">
      Table-type nested serializers not supported for direct rendering yet. Please create your own
      <b>as_component_def_table()</b> function and appropriate <b>visual component</b>.
    </v-alert>
  </v-input>
</template>

<script setup lang="ts">
import { BaseEmits, BaseProps, useInputBase } from './base-composable';

interface Props extends BaseProps {}
const props = defineProps<Props>();

interface Emits extends BaseEmits {}
const emits = defineEmits<Emits>();

const { baseBinds } = useInputBase(props, emits);

</script>
