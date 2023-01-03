<template>
  <div>
    <div v-for="(row, row_index) in column.rows" :key="row_index" class="sub-row">
      <GenericColumn
        v-for="field in row.fields"
        :key="field.name"
        :column="field"
        :row-data="rowData"
        :row-type="rowType"
        :thead="thead"
        :actions="actions"
      />
    </div>
  </div>
</template>

<script lang="ts">
import { defineComponent } from 'vue';

import FilteredActions from '@/components/actions/filtered-actions';

import TableColumn from '@/components/table/definitions/column';
import RenderMeasureMixin from '@/components/table/render-measure.mixin';
import RowTypesMixin from '@/components/table/row-types.mixin';

export default defineComponent({
  name: 'ColumnGroup',
  mixins: [RenderMeasureMixin, RowTypesMixin],
  props: {
    column: { type: TableColumn, required: true },
    rowData: { type: Object, required: true },
    actions: { type: FilteredActions, default: null },
  },
  methods: {
    onMeasure(refName: string, maxWidth: number) {
      if (refName === 'column') {
        this.column.setMaxWidth(maxWidth);
      }
    },
  },
});
</script>

<style scoped>

</style>
