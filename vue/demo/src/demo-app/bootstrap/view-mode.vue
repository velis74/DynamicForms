<template>
  <div>
    <b-row align-h="center" class="my-4">
      <b-form-checkbox-group
        v-model="viewModeChecked"
        :options="viewModeOptions"
        buttons
        @change="changeViewMode"
      />
    </b-row>
    <component :is="componentName" v-if="componentName" v-bind="data"/>
  </div>
</template>

<script lang="ts">
import { defineComponent } from 'vue';

import ConsumerLogicApi from '@velis/dynamicforms/src/components/api_consumer/consumer-logic-api';

// import DFForm from '../components/bootstrap/form/dfform.vue';
// import DynamicForms from '../dynamicforms';
// import actionHandlerMixin from '../mixins/actionHandlerMixin';

export default /* #__PURE__ */ defineComponent({
  name: 'BootstrapViewMode',
  emits: ['title-change', 'load-route'],
  data() {
    return {
      viewModes: ['form', 'table', 'dialog'],
      uuid: 'the-three-modes',
      viewModeChecked: ['form'],
      oldViewModeChecked: ['form'],
      consumer: new ConsumerLogicApi('/hidden-fields'),
      data: {},
    };
  },
  computed: {
    viewMode() { return this.viewModeChecked[0]; },
    viewModeOptions() { return this.viewModes.map((option) => ({ text: option, value: option })); },
    hasData() { return Object.keys(this.data).length !== 0; },
    showForm() { return this.viewMode === 'form'; },
    showTable() { return this.viewMode === 'table'; },
    showDialog() { return this.viewMode === 'dialog'; },
    componentName() {
      if (!this.hasData) return null;
      if (this.showTable && this.data) return 'df-table';
      if (this.showForm && this.data) return 'df-form';
      return null;
    },
  },
  mounted() {
    this.$emit('title-change', 'The three view-modes');
    this.$emit('load-route', 'view-mode', '');
  },
  created() {
    this.setViewMode();
  },
  methods: {
    changeViewMode() {
      this.oldViewModeChecked = this.viewModeChecked.filter((item) => !this.oldViewModeChecked.includes(item));
      this.viewModeChecked = [...this.oldViewModeChecked];
      this.setViewMode();
    },
    async setViewMode() {
      try {
        this.loading = true;
        this.$emit('title-change', 'The three view-modes');
        this.data = {};
        if (this.showTable) {
          await this.consumer.getFullDefinition();
          this.data = this.consumer.tableDefinition;
        } else if (this.showForm) {
          this.data = await this.consumer.getFormDefinition('new');
        } /* else {
          TODO: uncomment when modal has fromURL() method
          await DynamicForms.dialog.fromURL(`${this.url}/new.componentdef`, 'new', this.uuid);
          this.setViewMode('table');
        } */
      } finally {
        this.loading = false;
      }
    },
  },
});
</script>
