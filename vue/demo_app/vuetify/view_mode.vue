<template>
  <div>
    <v-row justify="center" class="my-4">
      <v-btn-toggle v-model="viewMode" mandatory @change="setViewMode">
        <v-btn v-for="mode in viewModes" :key="mode" :value="mode">{{ mode }}</v-btn>
      </v-btn-toggle>
      <!-- <Form form-p-k="new" :data="data" :show-form="showForm" :show-table="showTable"/> -->
    </v-row>
    {{ componentName }}
    <component :is="componentName" v-if="componentName" v-bind="data"/>
  </div>
</template>

<script>
import APIConsumerLogic from '../../components/api_consumer/api_consumer_logic';
import { DfForm, DfTable } from '../../components/public';

// import DFForm from '../components/bootstrap/form/dfform.vue';
// import DynamicForms from '../dynamicforms';
// import actionHandlerMixin from '../mixins/actionHandlerMixin';

export default {
  name: 'VuetifyViewMode',
  components: { DfForm, DfTable },
  emits: ['title-change', 'load-route'],
  data() {
    return {
      viewModes: ['form', 'table', 'dialog'],
      uuid: 'the-three-modes',
      viewMode: 'form',
      consumer: new APIConsumerLogic('/hidden-fields'),
      data: {},
    };
  },
  computed: {
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
    async setViewMode() {
      try {
        this.loading = true;
        this.$emit('title-change', 'The three view-modes');
        this.data = {};
        if (this.showTable) {
          await this.consumer.getFullDefinition();
          this.data = this.consumer.tableDefinition;
        } else if (this.showForm) {
          await this.consumer.getFormDefinition('new');
          this.data = this.consumer.formDefinition;
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
};
</script>
