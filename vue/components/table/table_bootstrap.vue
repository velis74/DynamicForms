<template>
  <v-card>
    <v-card-title>{{ title }}</v-card-title>
    <v-card-text>
      <component :is="'style'" :key="tableStyle" scoped v-html="tableStyle"/>
      <div :id="uniqueId" ref="container">
        <BootstrapTHead :rendered-columns="responsiveColumns"/>
        <BootstrapTBody
          :data-columns="dataColumns"
          :rendered-columns="responsiveColumns"
          :rows="rows"
          :pk-name="pkName"
        />
      </div>
      <LoadingIndicator :loading="loading"/>
      <div v-if="!loading && rows.data.length === 0" class="nodata">{{ gettext('No data') }}</div>
    </v-card-text>
  </v-card>
</template>
<script>
import LoadingIndicator from '../util/loading_indicator';

import Table from './table';
import BootstrapTBody from './tbody_generic';
import BootstrapTHead from './thead_generic';

export default {
  name: 'BootstrapTable',
  components: { BootstrapTHead, BootstrapTBody, LoadingIndicator },
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
