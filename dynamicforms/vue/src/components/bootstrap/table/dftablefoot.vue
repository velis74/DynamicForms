<template>
  <tfoot>
    <tr v-if="rows.length === 0 && !loading" class="no-data-indicator">
      <td :colspan="columns.length">{{ noDataString }}</td>
    </tr>
    <tr v-if="rows.length === 0 && loading" class="no-data-indicator">
      <td :colspan="columns.length">
        <div class="lds-ellipsis">
          <div/>
          <div/>
          <div/>
          <div/>
        </div>
      </td>
    </tr>
    <DFTableLoadingIndicator :loading="loading" :rows="rows" :columns="columns"/>
  </tfoot>
</template>

<script>
import DFTableLoadingIndicator from './dftableloadingindicator.vue';

export default {
  name: 'DFTableFoot',
  components: { DFTableLoadingIndicator },
  props: {
    columns: { type: Array, required: true },
    rows: { type: Array, required: true },
    loading: { type: Boolean, required: true },
    noDataString: { type: String, required: true },
  },
};
</script>

<style scoped>

</style>
