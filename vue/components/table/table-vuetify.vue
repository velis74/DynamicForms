<template>
  <v-card flat>
    <v-card-title>{{ title }}</v-card-title>
    <v-card-text :key="responsiveLayoutWidth">
      <!-- eslint-disable vue/no-v-text-v-html-on-component -->
      <table-style :columns="responsiveColumns" :unique-id="uniqueId"/>
      <!-- eslint-enable -->
      <div :id="uniqueId" ref="container">
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
<!--suppress ES6UnusedImports -->
<script lang="ts">
import { defineComponent, defineProps, withDefaults } from 'vue';

import VuetifyActions from '../actions/actions-vuetify.vue';
import FilteredActions from '../actions/filtered-actions';
import LoadingIndicator from '../util/loading-indicator.vue';
import TranslationsMixin from '../util/translations-mixin';

import TableColumn from './definitions/column';
import TableFilterRow from './definitions/filterrow';
import TableRows from './definitions/rows';
import RenderMeasured from './render-measure';
import { useTableBase } from './table';
import TableStyle from './table-style.vue';
import VuetifyTBody from './tbody-generic.vue';
import VuetifyTHead from './thead-generic.vue';

export default /* #__PURE__ */ defineComponent({
  name: 'VuetifyTable',
  components: { LoadingIndicator, VuetifyActions, VuetifyTHead, VuetifyTBody, TableStyle },
  mixins: [RenderMeasured, TranslationsMixin],
  setup() {
  },
});
</script>
<script setup lang="ts">

const props = withDefaults(
  defineProps<{ // Can't just import the interface - vue complains. https://github.com/vuejs/core/issues/4294
    pkName: string;
    title: string;
    columns: TableColumn[];
    responsiveTableLayouts: object | null;
    columnDefs: object;
    rows: TableRows;
    loading: boolean;
    actions: FilteredActions;
    filterDefinition: TableFilterRow | null;
  }>(),
  {
    responsiveTableLayouts: null,
    loading: false,
    filterDefinition: null,
  },
);

// const { pkName, title, rows, loading, actions, filterDefinition } = toRefs(props);
const {
  uniqueId,
  container,
  responsiveLayoutWidth,
  responsiveColumns,
  responsiveLayout, // eslint-disable-line @typescript-eslint/no-unused-vars
  dataColumns,
  theadRowData,
  onMeasure, // eslint-disable-line @typescript-eslint/no-unused-vars
} = useTableBase(props);
</script>

<style scoped>
.nodata {
  min-height:  4em;
  line-height: 4em;
  text-align:  center;
  font-size:   200%;
}
</style>
