<template>
  <label v-if="def.label" :id="`label-${def.uuid}`" :for="def.uuid">{{ def.label }}</label>
</template>

<script>

export default {
  name: 'DFWidgetBaseLabel',
  props: {
    def: { type: Object, required: true },
    data: { type: Object, required: false, default: () => {} },
  },
};
</script>

<style scoped>

</style>
