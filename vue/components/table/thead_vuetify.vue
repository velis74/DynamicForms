<template>
  <div class="df-thead">
    <div class="df-row">
      <div
        v-for="column in renderedColumns"
        :key="column.name"
        :ref="column.name"
        :class="`df-col text-${column.align}`"
      >
        {{ column.label }}
      </div>
    </div>
    <div class="df-separator"/>
  </div>
</template>
<script>
import RenderMeasured from './measure-render';

export default {
  name: 'VuetifyTHead',
  mixins: [RenderMeasured],
  props: { renderedColumns: { type: Array, required: true } },
};
</script>
