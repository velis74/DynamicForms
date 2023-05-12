<template>
  <div>
    <component :is="renderComponent" v-bind="renderComponentData"/>
  </div>
</template>
<script lang="ts">
import { defineComponent } from 'vue';

import Action from '../actions/action';
import FormPayload from '../form/definitions/form-payload';
import TableColumn from '../table/definitions/column';
import RowTypes from '../table/definitions/row-types';

import ComponentDisplay from './component-display';
import ConsumerLogicBase from './consumer-logic-base';

export default defineComponent({
  name: 'APIConsumer',
  props: {
    /**
     * Object containing the properties required to render at least one of the display components
     *
     * TODO: APIConsumerBase is not reactive. you have to assign the object anew for APIConsumer to work.
     *  It won't do to just call .getFullDefinition on an existing object.
     *
     * TODO: APIConsumer is named incorrectly, causing <a-p-i-consumer> component name. Rename.
     */
    consumer: { type: Object, required: true, validator: (value: Object) => value instanceof ConsumerLogicBase },
    /**
     * What UX should the component render
     */
    displayComponent: {
      type: Number,
      required: true,
      validator(value: ComponentDisplay) { return ComponentDisplay.isDefined(value); },
    },
  },
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
    actionDelete(actionData: Action, payload: FormPayload) {
      this.consumer.deleteRow(payload);
      return true;
    },
    actionValueChanged(actionData: Action, payload: FormPayload) {
      this.consumer.filter(payload);
      return true;
    },
    async actionAdd() {
      await this.consumer.dialogForm('new');
      return true;
    },
    async actionEdit(
      actionData: Action,
      payload: FormPayload | undefined | null,
      extraData: { rowType: RowTypes },
    ) {
      // eslint-disable-next-line eqeqeq
      if (extraData.rowType !== RowTypes.Data || payload == undefined) return false;
      await this.consumer.dialogForm(payload[this.consumer.pkName]);
      return true;
    },
    actionSort(
      actionData: Action,
      payload: FormPayload,
      extraData: { rowType: RowTypes, column?: TableColumn, event: KeyboardEvent },
    ) {
      // This is the default handler for ordering
      if (extraData.rowType === RowTypes.Label && actionData.position === 'ROW_CLICK' && extraData.column) {
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
