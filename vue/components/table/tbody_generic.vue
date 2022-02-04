<template>
  <div>
    <div v-for="row in rows" :key="row[pkName]" class="df-row">
      <div
        v-for="column in renderedColumns"
        :key="column.name"
        :ref="column.name"
        :class="`df-col text-${column.align}`"
      >
        {{ row[column.name] }}
      </div>
    </div>
  </div>
</template>
<script>
import RenderMeasured from './measure-render';

export default {
  name: 'VuetifyTBody',
  mixins: [RenderMeasured],
  props: {
    pkName: { type: String, required: true },
    renderedColumns: { type: Array, required: true },
    dataColumns: { type: Array, required: true },
    rows: { type: Array, required: true },
  },
};
</script>
