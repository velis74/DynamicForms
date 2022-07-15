<template>
  <div>
    <component :is="renderComponent" v-bind="renderComponentData"/>
  </div>
</template>
<script>
import { DfForm, DfModal, DfTable } from '../public';

import APIConsumerLogic from './api_consumer_logic';
import ComponentDisplay from './component_display';

export default {
  name: 'APIConsumer',
  components: { DfModal, DfForm, DfTable },
  props: {
    /**
     * Object containing the properties required to render at least one of the display components
     */
    consumer: { type: APIConsumerLogic, required: true },
    /**
     * What UX should the component render
     */
    displayComponent: { type: Object, required: true, validator(value) { return ComponentDisplay.isDefined(value); } },
  },
  data() { return { orderingCounter: this.consumer.ordering.counter.counter }; },
  computed: {
    renderComponent() {
      switch (this.displayComponent) {
      case ComponentDisplay.TABLE:
        return 'df-table';
      case ComponentDisplay.FORM:
        return 'df-form';
      case ComponentDisplay.DIALOG:
        return 'df-modal';
      default:
        throw Error('Unknown component display type');
      }
    },
    renderComponentData() {
      switch (this.displayComponent) {
      case ComponentDisplay.TABLE:
        return this.consumer.tableDefinition;
      default:
        throw Error('Unknown component display type');
      }
    },
  },
  methods: {
    actionDelete(actionData, payload) {
      this.consumer.deleteRow(payload);
      return true;
    },
    actionValuechanged(actionData) {
      this.consumer.filter(actionData);
    },
  },
  watch: {
    'consumer.ordering': {
      handler() {
        if (this.orderingCounter !== this.consumer.ordering.counter.counter) {
          this.consumer.reload();
        }
      },
      deep: true,
    },
  },
};
</script>
