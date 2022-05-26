<template>
  <v-card>
    <v-card-title>{{ title }}</v-card-title>
    <v-card-text>
      <component :is="'style'" :key="tableStyle" scoped v-html="tableStyle"/>
      <div :id="uniqueId" ref="container" :key="responsiveLayoutWidth">
        <VuetifyActions :actions="actions.header()"/>
        <VuetifyTHead
          :rendered-columns="responsiveColumns"
          :filter-definition="filterDefinition"
          :row-data="theadRowData"
          :actions="actions"
        />
        <VuetifyTBody
          :data-columns="dataColumns"
          :rendered-columns="responsiveColumns"
          :rows="rows"
          :actions="actions"
          :pk-name="pkName"
        />
        <LoadingIndicator :loading="loading"/>
        <div v-if="!loading && rows.data.length === 0" class="nodata">{{ gettext('No data') }}</div>
      </div>
    </v-card-text>
  </v-card>
</template>
<script>
import VuetifyActions from '../actions/actions_vuetify';
import LoadingIndicator from '../util/loading_indicator';

import Table from './table';
import VuetifyTBody from './tbody_generic';
import VuetifyTHead from './thead_generic';

export default {
  name: 'VuetifyTable',
  components: { LoadingIndicator, VuetifyActions, VuetifyTHead, VuetifyTBody },
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
