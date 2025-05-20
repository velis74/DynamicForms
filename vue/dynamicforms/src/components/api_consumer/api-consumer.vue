<template>
  <div style="flex: auto">
    <component
      :is="renderComponent"
      v-bind="renderComponentData"
      :sub-handlers="handlers?.subhandlers"
      :dialog-sub-handlers="dialogHandlers?.subhandlers"
    />
  </div>
</template>

<script setup lang="ts">
import { computed, watch } from 'vue';

import Action from '../actions/action';
import { useActionHandler } from '../actions/action-handler-composable';
import type { ActionsNS } from '../actions/namespace';
import FormPayload from '../form/definitions/form-payload';
import dfModal from '../modal/modal-view-api';
import TableColumn from '../table/definitions/column';
import RowTypes from '../table/definitions/row-types';
import { gettext, interpolate } from '../util/translations-mixin';

import ComponentDisplay from './component-display';
import ConsumerLogicBase from './consumer-logic-base';
import FormConsumerBase from './form-consumer/base';
import { APIConsumer } from './namespace';

type IHandlers = ActionsNS.IHandlers;

/**
 * Object containing the properties required to render at least one of the display components
 *
 * TODO: APIConsumerBase is not reactive. you have to assign the object anew for APIConsumer to work.
 *  It won't do to just call .getFullDefinition on an existing object.
 *
 * TODO: APIConsumer is named incorrectly, causing <a-p-i-consumer> component name. Rename.
 */

const props = defineProps<{
  consumer: APIConsumer.ConsumerLogicBaseInterface | FormConsumerBase,
  displayComponent: ComponentDisplay,
  handlers?: IHandlers,
  dialogHandlers?: IHandlers,
}>();

if (!ComponentDisplay.isDefined(props.displayComponent)) {
  console.warn(
    interpolate(
      'ApiConsumer.displayComponent property has an unsupported value \'%(component)s\'',
      { component: props.displayComponent },
    ),
  );
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

const displayComponent = computed(() => props.displayComponent);
const renderComponentData = computed(() => {
  switch (displayComponent.value) {
  case ComponentDisplay.TABLE:
    return (<APIConsumer.ConsumerLogicBaseInterface>props.consumer).tableDefinition;
  case ComponentDisplay.FORM:
    // console.warn(props.consumer.formDefinition);
    return (<FormConsumerBase>props.consumer).definition;
    // TODO: what about dialog? Where is this APIConsumer even used?
    // TODO: And why isn't APIConsumer used on the page which showcases the three input modes. What's there instead?
  default:
    throw Error('Unknown component display type');
  }
});

const { handler } = useActionHandler();

if (props.consumer instanceof ConsumerLogicBase) {
  (<APIConsumer.ConsumerLogicBaseInterface>props.consumer).setDialogHandlers(props.dialogHandlers);
}

async function actionDelete(actionData: Action, payload: FormPayload) {
  const res = await dfModal.yesNo(gettext('Delete'), gettext('Are you sure you want to delete this record?'));
  if (res.action.name.toUpperCase() === 'YES') {
    await (<APIConsumer.ConsumerLogicBaseInterface>props.consumer).deleteRow(payload);
  }
  return true;
}

function actionValueChanged(actionData: Action, payload: FormPayload) {
  if (props.displayComponent === ComponentDisplay.TABLE) {
    (<APIConsumer.ConsumerLogicBaseInterface>props.consumer).filter(payload);
  }
  return true;
}

async function actionAdd() {
  await (<APIConsumer.ConsumerLogicBaseInterface>props.consumer).dialogForm('new');
  return true;
}

async function actionEdit(
  actionData: Action,
  payload: FormPayload | undefined | null,
  context: { rowType: RowTypes },
) {
  if (context.rowType !== RowTypes.Data || payload == undefined) return false; // eslint-disable-line eqeqeq
  await (<APIConsumer.ConsumerLogicBaseInterface>props.consumer).dialogForm(payload[props.consumer.pkName]);
  return true;
}

function actionSort(
  actionData: Action,
  payload: FormPayload,
  context: { rowType: RowTypes, column?: TableColumn, event: MouseEvent },
) {
  // This is the default handler for ordering
  if (context.rowType === RowTypes.Label && actionData.position === 'ROW_CLICK' && context.column) {
    const oldChangeCounter = context.column.ordering.changeCounter;
    context.column.ordering.handleColumnHeaderClick(context.event);
    if (oldChangeCounter !== context.column.ordering.changeCounter) {
      (<APIConsumer.ConsumerLogicBaseInterface>props.consumer).reload();
    }
    return true;
  }
  return false;
}

const actionCancel = async (): Promise<boolean> => {
  await (<FormConsumerBase>props.consumer).getUXDefinition();
  return true;
};

const actionSubmit = async (): Promise<boolean> => {
  try {
    await (<FormConsumerBase>props.consumer).save();
    (<FormConsumerBase>props.consumer).withErrors({});
  } catch (err: any) {
    (<FormConsumerBase>props.consumer).withErrors({ ...err?.response?.data });
    return true;
  }
  await (<FormConsumerBase>props.consumer).getUXDefinition();
  return true;
};

function checkConsumerCorrectness() {
  if (props.displayComponent === ComponentDisplay.FORM) {
    if (!(props.consumer instanceof FormConsumerBase)) {
      console.error('Showing FORM requires a FormConsumerBase consumer, but the provided one is not', props.consumer);
    }
  }
  if (props.displayComponent === ComponentDisplay.TABLE) {
    if (props.consumer instanceof FormConsumerBase) {
      console.error('Showing TABLE requires a ConsumerLogicBase consumer, but the provided one is not', props.consumer);
    }
  }
}

checkConsumerCorrectness();

watch(() => props.displayComponent, checkConsumerCorrectness);

const defaultHandlers: IHandlers = {
  delete: actionDelete,
  value_changed: actionValueChanged,
  sort: actionSort,
  add: actionAdd,
  edit: actionEdit,
  cancel: actionCancel, // when displayComponent == ComponentDisplay.FORM
  submit: actionSubmit, // when displayComponent == ComponentDisplay.FORM
};

for (const key of Object.keys({ ...defaultHandlers, ...props.handlers })) {
  handler.register(key, async (
    action: Action,
    payload: FormPayload,
    context: any,
  ) => (
    await props?.handlers?.[key]?.(action, payload, context) ||
    await defaultHandlers?.[key]?.(action, payload, context)
  ));
}
</script>
