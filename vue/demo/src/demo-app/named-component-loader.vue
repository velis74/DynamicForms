<script setup lang="ts">
defineProps<{
  componentName: string,
  componentProps: object,
}>();

const emits = defineEmits(['title-change']);
</script>

<template>
  <component
    :is="componentName"
    :v-bind="componentProps"
    @title-change="(title: string) => emits('title-change', title)"
  />
</template>
