<template>
  <div class="card">
    <div class="card-header">
      {{ configuration.tableLabel }}
      <div class="float-right">
        <Actions :actions="actions.filter('HEADER')"/>
      </div>
    </div>
    <div class="card-body">
      <table :id="'DFTable' + tableID" class="table">
        <DFTableHead :columns="columns" :filter="filter" :table-id="tableID" @setTableFilter="setTableFilter"/>
        <DFTableBody :columns="columns" :rows="rows" :actions="actions"/>
        <DFTableFoot :columns-length="colsLen" :rows-length="rowsLen" :loading="loading" :no-data-label="noDataLabel"/>
      </table>
    </div>
  </div>
</template>

<script>
import Actions from '../actions.vue';

import DFTableBody from './dftablebody.vue';
import DFTableFoot from './dftablefoot.vue';
import DFTableHead from './dftablehead.vue';

let globalTableID = 0;

export default {
  name: 'BootstrapTable',
  components: {
    DFTableFoot, DFTableHead, DFTableBody, Actions,
  },
  props: {
    configuration: { type: Object, required: true },
  },
  data() {
    return {
      style: null,
      tableID: globalTableID++,
    };
  },
  computed: {
    actions: function actions() { return this.configuration.actions; },
    filter: function filter() { return this.configuration.filter; },
    columns: function columns() { return this.configuration.columns; },
    rows: function rows() { return this.configuration.rows; },
    colsLen: function colsLen() { return this.configuration.columns.length; },
    rowsLen: function rowsLen() { return this.configuration.rows.length; },
    loading: function loading() { return this.configuration.loading; },
    noDataLabel: function noDataLabel() { return this.configuration.noDataString; },
  },
  methods: {
    setTableFilter(filter) {
      this.$emit('setTableFilter', filter);
    },
  },
};
</script>

<style scoped>

</style>
