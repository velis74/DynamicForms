<template>
  <div v-if="hasData && showForm" class="card">
    <div class="card-header">{{ title }}</div>
    <div class="card-body">
      <component :is="component" :rows="layout" :uuid="uuid" :record="record"/>
    </div>
    <div class="card-footer text-right">
      <button
        v-for="button in buttons"
        :id="button.element_id || button.uuid"
        :key="button.uuid"
        type="button"
        :class="button.classes"
        v-bind="button.arias"
        @click.stop="buttonClick($event, button)"
      >
        {{ button.label }}
      </button>
    </div>
  </div>
  <DFTable v-else-if="hasData && showTable" :config="data"/>
  <DFLoadingIndicator v-else :loading="loading"/>
</template>

<script>
import eventBus from '../../../logic/eventBus';
import DFLoadingIndicator from '../loadingindicator.vue';

export default {
  name: 'DFForm',
  components: {
    DFLoadingIndicator,
    DFFormLayout: () => import('./dfformlayout.vue'),
    DFTable: () => import('../../dftable.vue'),
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
    buttons() {
      const cDef = this.data;
      const actions = cDef.dialog.actions;
      return Object.keys(cDef.dialog.actions)
        .filter((key) => cDef.dialog.actions[key].name !== 'form_init' && cDef.dialog.actions[key].name !== 'cancel')
        .reduce(
          (res, key) => {
            actions[key].data_return = { dialog_id: cDef.uuid, button: actions[key] };
            res.push(actions[key]);
            return res;
          }, [],
        );
    },
  },
  methods: {
    buttonClick($event, button) {
      eventBus.$emit(`tableActionExecuted_${this.uuid}`, {
        action: button,
        data: this.data.record,
        modal: null,
        $event,
        promise: null,
      });
    },
  },
};
</script>

<style scoped>

</style>
