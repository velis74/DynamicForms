<template>
  <div>
    <component :is="renderComponent" v-bind="renderComponentData"/>
  </div>
</template>
<script lang="ts">
import { defineComponent } from 'vue';

import RowTypesEnum from '../table/row-types-enum';

import APIConsumerLogic from './api-consumer-logic';
import ComponentDisplay from './component-display';

export default /* #__PURE__ */ defineComponent({
  name: 'APIConsumer',
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
  methods: {
    actionDelete(actionData, payload) {
      this.consumer.deleteRow(payload);
      return true;
    },
    actionValueChanged(actionData, payload) {
      this.consumer.filter(payload);
      return true;
    },
    async actionAdd() {
      await this.consumer.dialogForm('new');
      return true;
    },
    async actionEdit(actionData, payload, extraData) {
      if (extraData.rowType !== RowTypesEnum.Data) return false;
      await this.consumer.dialogForm(payload[this.consumer.pkName]);
      return true;
    },
    actionSort(action, payload, extraData) {
      // This is the default handler for ordering
      if (extraData.rowType === RowTypesEnum.Label && action.position === 'ROW_CLICK' && extraData.column) {
        const oldChangeCounter = extraData.column.ordering.changeCounter;
        extraData.column.ordering.handleColumnHeaderClick(extraData.event);
        if (oldChangeCounter !== extraData.column.ordering.changeCounter) this.consumer.reload();
        return true;
      }
      return false;
    },
  },
});
</script>
