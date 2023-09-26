<template>
  <v-card flat>
    <v-card-title>{{ title }}</v-card-title>
    <v-card-text :key="responsiveLayoutWidth">
      <table-style :columns="responsiveColumns" :unique-id="uniqueId"/>
      <div :id="uniqueId" ref="container">
        <VuetifyActions :actions="actions.header"/>
        <VuetifyTHead
          :rendered-columns="responsiveColumns"
          :row-data="theadRowData"
          :actions="actions"
          :filter-definition="filterDefinition || undefined"
        />
        <VuetifyTBody
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

<script setup lang="ts">
import { defineComponent, toRefs } from 'vue';

import VuetifyActions from '../actions/actions-vuetify.vue';
import LoadingIndicator from '../util/loading-indicator.vue';
import TranslationsMixin from '../util/translations-mixin';

import { useRenderMeasure } from './render-measure';
import { useTableBase, TableBasePropsInterface } from './table';
import TableStyle from './table-style.vue';
import VuetifyTBody from './tbody-generic.vue';
import VuetifyTHead from './thead-generic.vue';

interface Props extends TableBasePropsInterface {}

const props = withDefaults(
  defineProps<Props>(),
  {
    responsiveTableLayouts: null,
    loading: false,
    filterDefinition: null,
  },
);

const { pkName, title, rows, loading, actions, filterDefinition } = toRefs(props);
const {
  uniqueId,
  container,
  responsiveLayoutWidth,
  responsiveColumns,
  responsiveLayout, // eslint-disable-line @typescript-eslint/no-unused-vars
  theadRowData,
  onMeasure,
} = useTableBase(props);

useRenderMeasure(onMeasure, { container });
</script>
<script lang="ts">
export default /* #__PURE__ */ defineComponent({
  name: 'VuetifyTable',
  mixins: [TranslationsMixin],
});
</script>

<style scoped>
.nodata {
  min-height:  4em;
  line-height: 4em;
  text-align:  center;
  font-size:   200%;
}
</style>
