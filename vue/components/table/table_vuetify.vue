<template>
  <v-card>
    <v-card-title>{{ title }}</v-card-title>
    <v-card-text>
      <component :is="'style'" :key="tableStyle" scoped v-html="tableStyle"/>
      <div :class="uniqueId">
        <VuetifyTHead :rendered-columns="renderedColumns" @render-measured="measureRenders"/>
        <VuetifyTBody
          :data-columns="dataColumns"
          :rendered-columns="renderedColumns"
          :rows="rows"
          :pk-name="pkName"
          @render-measured="measureRenders"
        />
        <LoadingIndicator :loading="loading"/>
        <div v-if="!loading && rows.data.length === 0" class="nodata">{{ gettext('No data') }}</div>
      </div>
    </v-card-text>
  </v-card>
</template>
<script>
import LoadingIndicator from '../util/loading_indicator';

import Table from './table';
import VuetifyTBody from './tbody_generic';
import VuetifyTHead from './thead_generic';

export default {
  name: 'VuetifyTable',
  components: { LoadingIndicator, VuetifyTHead, VuetifyTBody },
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
