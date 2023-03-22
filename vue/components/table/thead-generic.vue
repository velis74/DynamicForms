<template>
  <div ref="df-thead" class="df-thead">
    <GenericTRow
      :rendered-columns="renderedColumns"
      :data-columns="[]"
      :row-data="rowData"
      :actions="actions"
      :row-type="RowTypesEnum.Label"
    />
    <GenericTRow
      v-if="filterDefinition"
      :rendered-columns="renderedColumns"
      :data-columns="[]"
      :row-data="rowData"
      :actions="actions"
      :filter-definition="filterDefinition"
      :row-type="RowTypesEnum.Filter"
    />
    <div class="df-separator"/>
  </div>
</template>
<script lang="ts">
import { defineComponent } from 'vue';

import FilteredActions from '../actions/filtered-actions';
import IndexedArray from '../classes/indexed-array';

import TableFilterRow from './definitions/filterrow';
import TableRow from './definitions/row';
import RenderMeasured from './render-measure';
import RowTypesEnum from './row-types-enum';
import GenericTRow from './trow-generic.vue';

export default /* #__PURE__ */ defineComponent({
  name: 'GenericTHead',
  components: { GenericTRow },
  mixins: [RenderMeasured],
  props: {
    renderedColumns: { type: IndexedArray, required: true },
    rowData: { type: TableRow, required: true },
    actions: { type: FilteredActions, required: true },
    filterDefinition: { type: TableFilterRow, default: null },
    rowType: RowTypesEnum.rowTypeProp(),
  },
  data() { return { RowTypesEnum }; },
  computed: { thead() { return RowTypesEnum.isTHead(this.rowType); } },
  methods: {
    onMeasure(refName: string, maxWidth: number, maxHeight: number) {
      this.rowData.setMeasuredHeight(maxHeight);
    },
  },
});
</script>
