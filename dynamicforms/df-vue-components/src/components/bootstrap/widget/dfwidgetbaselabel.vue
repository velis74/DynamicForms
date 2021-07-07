<template>
  <label :for="def.uuid" :def="def" :data="data" v-if="def.label">{{ def.label }}</label>
</template>

<script>

export default {
  name: 'dfwidgetbaselabel',
  props: ['def', 'data'],
};
</script>

<style scoped>

</style>
