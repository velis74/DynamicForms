<template>
  <component :is="componentName" :v-bind="componentProps" @title-change="(title) => $emit('title-change', title)"/>
</template>

<script lang="ts">
import { defineComponent } from 'vue';

export default /* #__PURE__ */ defineComponent({
  name: 'NamedComponentLoader',
  props: {
    componentName: { type: String, required: true },
    componentProps: { type: Object, required: true },
  },
  emits: ['title-change'],
});
</script>
