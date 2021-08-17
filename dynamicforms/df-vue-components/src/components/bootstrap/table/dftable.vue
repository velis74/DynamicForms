<template>
  <div>
    <div class="card">
      <div class="card-header">{{ configuration.titles.table }}
        <div class="float-right">
          <Actions :actions="configuration.actions.filter('HEADER')"></Actions>
        </div>
      </div>
      <div class="card-body">
        <table class="table">
          <dftablehead :columns="configuration.columns" v-on:setTableFilter="setTableFilter"
                       :filter="configuration.filter"></dftablehead>
          <dftablebody :columns="configuration.columns"
                     :rows="configuration.rows"
                     :loading="configuration.loading"
                     :actions="configuration.actions"
          >
          </dftablebody>
          <dftablefoot :columns="configuration.columns"
                     :rows="configuration.rows"
                     :loading="configuration.loading"
                     :noDataString="configuration.noDataString"
          ></dftablefoot>
        </table>
      </div>
    </div>
  </div>
</template>

<script>
import dftablehead from '@/components/bootstrap/table/dftablehead.vue';
import dftablebody from '@/components/bootstrap/table/dftablebody.vue';
import dftablefoot from '@/components/bootstrap/table/dftablefoot.vue';
import Actions from '@/components/bootstrap/actions.vue';

export default {
  name: 'dftable',
  props: ['configuration'],
  methods: {
    setTableFilter(filter) {
      this.$emit('setTableFilter', filter);
    },
  },
  components: {
    dftablefoot, dftablehead, dftablebody, Actions,
  },
};
</script>

<style scoped>

</style>
