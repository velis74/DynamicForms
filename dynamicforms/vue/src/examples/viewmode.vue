<template>
  <div>
    <div class="btn-group">
      <div :class="`btn ${btnSelection('form')}`" @click="setViewMode('form')">form</div>
      <div :class="`btn ${btnSelection('table')}`" @click="setViewMode('table')">table</div>
      <div :class="`btn ${btnSelection('dialog')}`" @click="setViewMode('dialog')">dialog</div>
    </div>
    <DFForm form-p-k="new" :data="data" :show-form="showForm" :show-table="showTable"/>
  </div>
</template>

<script>
import apiClient from '../apiClient';
import DFForm from '../components/bootstrap/form/dfform.vue';
import DynamicForms from '../dynamicforms';
import actionHandlerMixin from '../mixins/actionHandlerMixin';

export default {
  name: 'PageLoader',
  components: { DFForm },
  mixins: [actionHandlerMixin],
  emits: ['title-change', 'load-route'],
  data() {
    return {
      url: '/hidden-fields',
      detail_url: '/hidden-fields/',
      uuid: 'the-three-modes',
      viewMode: 'form',
      data: {},
    };
  },
  computed: {
    showForm() { return this.viewMode === 'form'; },
    showTable() { return this.viewMode === 'table'; },
    showDialog() { return this.viewMode === 'dialog'; },
  },
  mounted() {
    this.$emit('title-change', 'The three view-modes');
    this.$emit('load-route', 'view-mode', '');
  },
  created() {
    this.setViewMode('form');
  },
  methods: {
    btnSelection(mode) {
      return this.viewMode === mode ? 'btn-primary' : 'btn-secondary';
    },
    async setViewMode(mode) {
      try {
        this.loading = true;
        this.viewMode = mode;
        this.data = {};
        if (this.showTable) {
          const url = `${this.url}.componentdef`;
          const data = await apiClient.get(url, { headers: { 'x-viewmode': 'TABLE_ROW', 'x-pagination': 1 } });
          this.data = data.data;
        } else if (this.showForm) {
          const url = `${this.url}/new.componentdef`;
          const data = await apiClient.get(url, { headers: { 'x-viewmode': 'FORM' } });
          this.data = data.data;
          this.data.uuid = this.uuid;
        } else {
          await DynamicForms.dialog.fromURL(`${this.url}/new.componentdef`, 'new', this.uuid);
          this.setViewMode('table');
        }
      } finally {
        this.loading = false;
      }
    },
  },
};
</script>
<style scoped>
.btn-group {
  margin-bottom: 1rem;
}
</style>
