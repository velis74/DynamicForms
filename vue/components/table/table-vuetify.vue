<template>
  <v-card flat>
    <v-card-title>{{ title }}</v-card-title>
    <v-card-text>
      <!-- eslint-disable vue/no-v-text-v-html-on-component -->
      <table-style :key="responsiveColumns.totalWidth" scoped :columns="responsiveColumns" :unique-id="uniqueId"/>
      <!-- eslint-enable -->
      <div :id="uniqueId" ref="container" :key="responsiveLayoutWidth">
        <VuetifyActions :actions="actions.header"/>
        <VuetifyTHead
          :rendered-columns="responsiveColumns"
          :row-data="theadRowData"
          :actions="actions"
          :filter-definition="filterDefinition"
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
<script lang="ts">
import { defineComponent } from 'vue';

import VuetifyActions from '../actions/actions-vuetify.vue';
import LoadingIndicator from '../util/loading-indicator.vue';

import Table from './table';
import TableStyle from './table-style.vue';
import VuetifyTBody from './tbody-generic.vue';
import VuetifyTHead from './thead-generic.vue';

export default /* #__PURE__ */ defineComponent({
  name: 'VuetifyTable',
  components: { LoadingIndicator, VuetifyActions, VuetifyTHead, VuetifyTBody, TableStyle },
  mixins: [Table],
});
</script>

<style scoped>
.nodata {
  min-height: 4em;
  line-height: 4em;
  text-align: center;
  font-size: 200%;
}
</style>
