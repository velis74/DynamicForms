<template>
  <v-card>
    <v-card-title>{{ title }}</v-card-title>
    <v-card-text>
      <component :is="'style'" :key="tableStyle" scoped v-html="tableStyle"/>
      <div :id="uniqueId" ref="container" :key="responsiveLayoutWidth">
        <VuetifyActions :actions="actions" :position="actionPositionHeader"/>
        <VuetifyTHead :rendered-columns="responsiveColumns" :row-data="theadRowData"/>
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
import Vue from 'vue';

import ActionUtils from '../actions/actions_util';
import VuetifyActions from '../actions/actions_vuetify';
import LoadingIndicator from '../util/loading_indicator';

import Table from './table';
import VuetifyTBody from './tbody_generic';
import VuetifyTHead from './thead_generic';

// Global registration is necessary: previous dynamic import was super-slow (see table.js)
Vue.component(VuetifyActions.name, VuetifyActions);

export default {
  name: 'VuetifyTable',
  components: { LoadingIndicator, VuetifyTHead, VuetifyTBody },
  mixins: [Table, ActionUtils],
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
