<template>
  <dfformcolumn v-if="isHiddenSingle" :def="columns[0]" :data="data"/>
  <div class="row" v-else>
    <dfformcolumn v-for="(column, idx) in columns" :key="idx" :def="column" :data="data"/>
  </div>
</template>

<script>
import DisplayMode from '@/logic/displayMode';
import dfformcolumn from '@/components/bootstrap/form/dfformcolumn.vue';

export default {
  name: 'formrow',
  props: ['columns', 'data'],
  computed: {
    isHiddenSingle() {
      return this.columns.length === 1 && this.columns[0].field.display === DisplayMode.HIDDEN;
    },
  },
  components: {
    dfformcolumn,
  },
};
</script>

<style scoped>

</style>
