<template>
  <div>
    <div class="card">
      <div class="card-header">
        {{ configuration.titles.table }}
        <div class="float-right">
          <Actions :actions="configuration.actions.filter('HEADER')"/>
        </div>
      </div>
      <div class="card-body">
        <table class="table">
          <DFTableHead
            :columns="configuration.columns"
            :filter="configuration.filter"
            @setTableFilter="setTableFilter"
          />
          <DFTableBody
            :columns="configuration.columns"
            :rows="configuration.rows"
            :loading="configuration.loading"
            :actions="configuration.actions"
          />
          <DFTableFoot
            :columns="configuration.columns"
            :rows="configuration.rows"
            :loading="configuration.loading"
            :no-data-string="configuration.noDataString"
          />
        </table>
      </div>
    </div>
  </div>
</template>

<script>
import Actions from '../actions.vue';

import DFTableBody from './dftablebody.vue';
import DFTableFoot from './dftablefoot.vue';
import DFTableHead from './dftablehead.vue';

export default {
  name: 'DFTable',
  components: {
    DFTableFoot, DFTableHead, DFTableBody, Actions,
  },
  props: {
    configuration: { type: Object, required: true },
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
