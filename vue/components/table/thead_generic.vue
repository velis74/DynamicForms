<template>
  <div ref="df-thead" class="df-thead">
    <div class="df-row">
      <div
        v-for="column in renderedColumns"
        :key="column.name"
        :ref="`col-${column.name}`"
        :class="`df-col text-${column.align}`"
      >
        {{ column.label }}
      </div>
    </div>
    <div class="df-separator"/>
  </div>
</template>
<script>
import RenderMeasured from './render_measure';

export default {
  name: 'GenericTHead',
  mixins: [RenderMeasured],
  props: { renderedColumns: { type: Array, required: true } },
};
</script>
