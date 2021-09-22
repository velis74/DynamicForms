<template>
  <label v-if="def.label" :id="`label-${def.uuid}`" :for="def.name" :class="def.render_params.label_class">
    {{ def.label }}
  </label>
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
