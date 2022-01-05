<template>
  <DFFormColumn
    v-if="isHiddenSingle"
    :def="writableColumns[0]"
    :data="data"
    :errors="errors"
  />
  <div v-else class="row align-items-end">
    <slot name="before-columns"/>
    <DFFormColumn
      v-for="(column, idx) in writableColumns"
      :key="idx"
      :def="column"
      :data="data"
      :errors="errors"
    />
    <slot name="after-columns"/>
  </div>
</template>

<script>
import DisplayMode from '../../../logic/displayMode';

import DFFormColumn from './dfformcolumn.vue';

export default {
  name: 'DFFormRow',
  components: {
    DFFormColumn,
  },
  props: {
    columns: { type: Array, required: true },
    data: { type: Object, required: true },
    errors: { type: Object, default: () => {} },
  },
  computed: {
    writableColumns() {
      return this.columns;
      // turns out we want to display read only columns, but they should be disabled. Displayed, but R/O
      // return this.columns.filter((col) => col.field.read_only !== true);
    },
    isHiddenSingle() {
      return this.writableColumns.length === 1 && this.writableColumns[0].field.visibility.form === DisplayMode.HIDDEN;
    },
  },
};
</script>

<style scoped>

</style>
