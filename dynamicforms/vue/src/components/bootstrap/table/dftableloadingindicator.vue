<template>
  <tr v-if="loading" class="loading-indicator">
    <td :colspan="columnsLength">
      <DFLoadingIndicator loading="loading"/>
    </td>
  </tr>
</template>

<script>
import _ from 'lodash/fp';

import DFLoadingIndicator from '../loadingindicator.vue';

export default {
  /**
   * Table row showing loading indicator
   */
  name: 'DFTableLoadingIndicator',
  components: { DFLoadingIndicator },
  props: {
    loading: { type: Boolean, required: true, validator: function v(loading) { return _.isBoolean(loading); } },
    columnsLength: { type: Number, required: true, validator: function v(len) { return _.isNumber(len); } },
  },
};
</script>

<style scoped>
tfoot tr.loading-indicator td {
  text-align: center;
}
</style>
