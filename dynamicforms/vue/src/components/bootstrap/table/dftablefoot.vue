<template>
  <tfoot>
    <tr v-if="rowsLength === 0 && !loading" class="no-data-indicator">
      <td :colspan="columnsLength">{{ noDataLabel }}</td>
    </tr>
    <DFTableLoadingIndicator v-else :loading="loading" :columns-length="columnsLength"/>
  </tfoot>
</template>

<script>
import _ from 'lodash/fp';

import DFTableLoadingIndicator from './dftableloadingindicator.vue';

export default {
  name: 'DFTableFoot',
  components: { DFTableLoadingIndicator },
  props: {
    loading: { type: Boolean, required: true, validator: function v(loading) { return _.isBoolean(loading); } },
    columnsLength: { type: Number, required: true, validator: function v(len) { return _.isNumber(len); } },
    rowsLength: { type: Number, required: true, validator: function v(len) { return _.isNumber(len); } },
    noDataLabel: { type: String, required: true, validator: function v(s) { return _.isString(s) && s.length > 0; } },
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
</style>
