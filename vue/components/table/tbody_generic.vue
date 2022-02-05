<template>
  <div>
    <div
      v-for="row in rows.data"
      :key="row[pkName]"
      v-observe-visibility="rows.visibilityHandler(row.id)"
      class="df-row"
    >
      <div
        v-for="column in renderedColumns"
        :key="column.name"
        :ref="`col-${column.name}`"
        :class="`df-col text-${column.align}`"
      >
        {{ row[column.name] }}
      </div>
    </div>
  </div>
</template>
<script>
import { ObserveVisibility } from 'vue-observe-visibility';

import TableRows from '../api_consumer/table_rows';

import RenderMeasured from './render_measure';

export default {
  name: 'GenericTBody',
  directives: { 'observe-visibility': ObserveVisibility },
  mixins: [RenderMeasured],
  props: {
    pkName: { type: String, required: true },
    renderedColumns: { type: Array, required: true },
    dataColumns: { type: Array, required: true },
    rows: { type: TableRows, required: true },
  },
};
</script>
