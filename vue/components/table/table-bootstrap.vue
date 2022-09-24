<template>
  <v-card>
    <v-card-title>{{ title }}</v-card-title>
    <v-card-text>
      <component :is="'style'" :key="tableStyle" scoped v-html="tableStyle"/>
      <div :id="uniqueId" ref="container" :key="responsiveLayoutWidth">
        <BootstrapActions :actions="actions.header"/>
        <BootstrapTHead :rendered-columns="responsiveColumns" :row-data="theadRowData"/>
        <BootstrapTBody
          :data-columns="dataColumns"
          :rendered-columns="responsiveColumns"
          :rows="rows"
          :actions="actions"
          :pk-name="pkName"
        />
      </div>
      <LoadingIndicator :loading="loading"/>
      <div v-if="!loading && rows.data.length === 0" class="nodata">{{ gettext('No data') }}</div>
    </v-card-text>
  </v-card>
</template>
<script>
import BootstrapActions from '../actions/actions-bootstrap';
import LoadingIndicator from '../util/loading-indicator';

import Table from './table';
import BootstrapTBody from './tbody-generic';
import BootstrapTHead from './thead-generic';

export default {
  name: 'BootstrapTable',
  components: { BootstrapActions, BootstrapTHead, BootstrapTBody, LoadingIndicator },
  mixins: [Table],
};
</script>

<style scoped>
.nodata {
  min-height:  4em;
  line-height: 4em;
  text-align:  center;
  font-size:   200%;
}
</style>
