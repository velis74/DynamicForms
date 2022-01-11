<template>
  <div v-if="hasData && showForm" class="card">
    <div class="card-header">{{ title }}</div>
    <div class="card-body">
      <component :is="component" :rows="layout" :uuid="uuid" :record="record"/>
    </div>
  </div>
  <DFTable v-else-if="hasData && showTable" :config="data"/>
  <DFLoadingIndicator v-else :loading="loading"/>
</template>

<script>
import DFLoadingIndicator from '@/components/bootstrap/loadingindicator.vue';

export default {
  name: 'DFForm',
  components: {
    DFLoadingIndicator,
    DFFormLayout: () => import('./dfformlayout.vue'),
    DFTable: () => import('@/components/dftable.vue'),
  },
  props: {
    formPK: { type: null, default: () => 'new' },
    showForm: { type: Boolean, default: true },
    showTable: { type: Boolean, default: false },
    data: { type: Object, default: () => { } },
  },
  data() {
    return {
      loading: false,
    };
  },
  computed: {
    hasData() { return Object.keys(this.data).length !== 0; },
    title() {
      if (this.data.titles) {
        if (this.showForm) return this.data.titles[this.formPK === 'new' ? 'new' : 'edit'];
        if (this.showTable) return this.data.titles.table;
      }
      return '';
    },
    layout() {
      return this.data.dialog ? this.data.dialog.rows : '';
    },
    uuid() {
      return this.data.uuid;
    },
    record() {
      return this.data.record;
    },
    component() {
      return this.data.dialog ? this.data.dialog.component_name : 'DFFormLayout';
    },
  },
};
</script>

<style scoped>

</style>
