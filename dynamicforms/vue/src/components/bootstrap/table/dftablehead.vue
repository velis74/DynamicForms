<template>
  <thead>
    <DFTableFilterRow v-if="filter" :configuration="filter" @setTableFilter="setTableFilter"/>
  </thead>
</template>

<script>
import DFTableFilterRow from './dftablefilterrow.vue';

export default {
  name: 'DFTableHead',
  components: { DFTableFilterRow },
  props: {
    columns: { type: Array, required: true },
    filter: { type: Object, default: () => {} },
    tableId: { type: Number, required: true },
  },
  methods: {
    setTableFilter(filter) {
      this.$emit('setTableFilter', filter);
    },
  },
};
</script>
