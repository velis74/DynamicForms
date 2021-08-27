<template>
  <tr class="loading-indicator" v-if="rows.length > 0 && loading">
    <td :colspan="columns.length">
      <dfloadingindicator loading="loading"/>
    </td>
  </tr>
</template>

<script>
import Dfloadingindicator from '../loadingindicator.vue';

export default {
  name: 'dftableloadingindicator',
  components: { Dfloadingindicator },
  props: {
    loading: {
      type: Boolean,
      required: true,
    },
    columns: {
      type: Array,
      required: true,
    },
    rows: {
      type: Array,
      required: true,
    },
  },
};
</script>

<style scoped>
  tfoot tr.no-data-indicator td {
    text-align: center;
    vertical-align: middle;
    height: 10em;
    background-color: #00000020; /* just darken a little */
  }

  tfoot tr.loading-indicator td {
    text-align: center;
  }
</style>
