<template>
  <div>
    <component :is="renderComponent" v-bind="renderComponentData"/>
  </div>
</template>

<script setup lang="ts">
import { computed } from 'vue';

import Action from '../actions/action';
import { useActionHandler } from '../actions/action-handler-composable';
import FormPayload from '../form/definitions/form-payload';
import TableColumn from '../table/definitions/column';
import RowTypes from '../table/definitions/row-types';

import ComponentDisplay from './component-display';
import { APIConsumer } from './namespace';

/**
 * Object containing the properties required to render at least one of the display components
 *
 * TODO: APIConsumerBase is not reactive. you have to assign the object anew for APIConsumer to work.
 *  It won't do to just call .getFullDefinition on an existing object.
 *
 * TODO: APIConsumer is named incorrectly, causing <a-p-i-consumer> component name. Rename.
 */

const props = defineProps<{
  consumer: APIConsumer.ConsumerLogicBaseInterface,
  displayComponent: ComponentDisplay,
}>();

if (!ComponentDisplay.isDefined(props.displayComponent)) {
  console.warn(`ApiConsumer.displayComponent property has an unsupported value '${props.displayComponent}'`);
}

const renderComponent = computed(() => {
  switch (props.displayComponent) {
  case ComponentDisplay.TABLE:
    return 'df-table';
  case ComponentDisplay.FORM:
    return 'df-form';
  case ComponentDisplay.DIALOG:
    return 'df-modal';
  default:
    throw Error('Unknown component display type');
  }
});

const renderComponentData = computed(() => {
  switch (props.displayComponent) {
  case ComponentDisplay.TABLE:
    return props.consumer.tableDefinition;
  case ComponentDisplay.FORM:
    // console.warn(props.consumer.formDefinition);
    return props.consumer.formDefinition;
    // TODO: what about dialog? Where is this APIConsumer even used?
    // TODO: And why isn't APIConsumer used on the page which showcases the three input modes. What's there instead?
  default:
    throw Error('Unknown component display type');
  }
});

const { handler } = useActionHandler();

function actionDelete(actionData: Action, payload: FormPayload) {
  props.consumer.deleteRow(payload);
  return true;
}

function actionValueChanged(actionData: Action, payload: FormPayload) {
  props.consumer.filter(payload);
  return true;
}

async function actionAdd() {
  await props.consumer.dialogForm('new');
  return true;
}

async function actionEdit(
  actionData: Action,
  payload: FormPayload | undefined | null,
  extraData: { rowType: RowTypes },
) {
  if (extraData.rowType !== RowTypes.Data || payload == undefined) return false; // eslint-disable-line eqeqeq
  await props.consumer.dialogForm(payload[props.consumer.pkName]);
  return true;
}

function actionSort(
  actionData: Action,
  payload: FormPayload,
  extraData: { rowType: RowTypes, column?: TableColumn, event: KeyboardEvent },
) {
  // This is the default handler for ordering
  if (extraData.rowType === RowTypes.Label && actionData.position === 'ROW_CLICK' && extraData.column) {
    const oldChangeCounter = extraData.column.ordering.changeCounter;
    extraData.column.ordering.handleColumnHeaderClick(extraData.event);
    if (oldChangeCounter !== extraData.column.ordering.changeCounter) props.consumer.reload();
    return true;
  }
  return false;
}

handler.register('delete', actionDelete)
  .register('value_changed', actionValueChanged)
  .register('sort', actionSort)
  .register('add', actionAdd)
  .register('edit', actionEdit);
</script>
