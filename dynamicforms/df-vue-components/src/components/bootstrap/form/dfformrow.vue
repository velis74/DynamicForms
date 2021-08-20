<template>
  <dfformcolumn v-if="isHiddenSingle" :def="writableColumns[0]" :data="data" :errors="errors"/>
  <div class="row align-items-end" v-else>
    <dfformcolumn v-for="(column, idx) in writableColumns" :key="idx" :def="column" :data="data" :errors="errors"/>
  </div>
</template>

<script>
import DisplayMode from '@/logic/displayMode';
import dfformcolumn from '@/components/bootstrap/form/dfformcolumn.vue';

export default {
  name: 'formrow',
  props: ['columns', 'data', 'errors'],
  computed: {
    writableColumns() {
      return this.columns.filter((col) => col.field.read_only !== true);
    },
    isHiddenSingle() {
      return this.writableColumns.length === 1 && this.writableColumns[0].field.visibility.form === DisplayMode.HIDDEN;
    },
  },
  components: {
    dfformcolumn,
  },
};
</script>

<style scoped>

</style>
