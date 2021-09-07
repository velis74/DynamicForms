<template>
  <tr v-if="rows.length > 0 && loading" class="loading-indicator">
    <td :colspan="columns.length">
      <DFLoadingIndicator loading="loading"/>
    </td>
  </tr>
</template>

<script>
import DFLoadingIndicator from '../loadingindicator.vue';

export default {
  name: 'DFTableLoadingIndicator',
  components: { DFLoadingIndicator },
  props: {
    loading: { type: Boolean, required: true },
    columns: { type: Array, required: true },
    rows: { type: Array, required: true },
  },
};
</script>

<style scoped>
tfoot tr.no-data-indicator td {
  text-align:       center;
  vertical-align:   middle;
  height:           10em;
  background-color: #00000020; /* just darken a little */
}

tfoot tr.loading-indicator td {
  text-align: center;
}
</style>
