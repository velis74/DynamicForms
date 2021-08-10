<template>
  <tfoot>
  <tr class="no-data-indicator" v-if="rows.length === 0 && !loading">
    <td :colspan="columns.length">{{ noDataString }}</td>
  </tr>
  <tr class="no-data-indicator" v-if="rows.length === 0 && loading">
    <td :colspan="columns.length">
      <div class="lds-ellipsis">
        <div></div>
        <div></div>
        <div></div>
        <div></div>
      </div>
    </td>
  </tr>
  <dftableloadingindicator :loading="loading" :rows="rows" :columns="columns"></dftableloadingindicator>
  </tfoot>
</template>

<script>
import dftableloadingindicator from '@/components/bootstrap/table/dftableloadingindicator.vue';

export default {
  name: 'dftablefoot',
  props: ['columns', 'rows', 'loading', 'noDataString'],
  components: {
    dftableloadingindicator,
  },
};
</script>

<style scoped>

</style>
