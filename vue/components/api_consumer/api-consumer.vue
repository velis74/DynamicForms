<template>
  <div>
    <component :is="renderComponent" v-bind="renderComponentData"/>
  </div>
</template>
<script>
import { DfForm, DfModal, DfTable } from '../public';
import RowTypesEnum from '../table/row-types-enum';

import APIConsumerLogic from './api-consumer-logic';
import ComponentDisplay from './component-display';

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
        // TODO: what about form and dialog? Where is this APIConsumer even used?
        // TODO: And why isn't APIConsumer used on the page which showcases the three input modes. What's there instead?
      default:
        throw Error('Unknown component display type');
      }
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
  methods: {
    actionDelete(actionData, payload) {
      this.consumer.deleteRow(payload);
      return true;
    },
    actionValueChanged(actionData) {
      this.consumer.filter(actionData);
      return true;
    },
    async actionAdd() {
      await this.consumer.dialogForm('new', this.$dfModal);
      return true;
    },
    async actionEdit(actionData, payload, extraData) {
      if (extraData.rowType !== RowTypesEnum.Data) return false;
      await this.consumer.dialogForm(payload[this.consumer.pkName], this.$dfModal);
      return true;
    },
    actionSort(action, payload, extraData) {
      // This is the default handler for ordering
      if (extraData.rowType === RowTypesEnum.Label && action.position === 'ROW_CLICK' && extraData.column) {
        extraData.column.ordering.handleColumnHeaderClick(extraData.event);
        return true;
      }
      return false;
    },
  },
};
</script>
