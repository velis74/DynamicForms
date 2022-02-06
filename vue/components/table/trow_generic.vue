<template>
  <div class="df-row">
    <div
      v-for="column in renderedColumns.items"
      :key="column.name"
      :ref="`col-${column.name}`"
      :class="`df-col text-${column.align}`"
    >
      {{ rowData[column.name] }}
    </div>
  </div>
</template>

<script>
import RenderMeasured from './render_measure';

export default {
  name: 'GenericTRow',
  mixins: [RenderMeasured],
  props: {
    renderedColumns: { type: Object, required: true },
    dataColumns: { type: Array, required: true },
    rowData: { type: Object, required: true },
  },
};
</script>
