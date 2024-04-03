import Action, { defaultActionHandler, getActionName } from '../actions/action';
import { IHandlers } from '../actions/action-handler-composable';
import FilteredActions from '../actions/filtered-actions';
import { APIConsumer } from '../api_consumer/namespace';

import DialogSize from './definitions/dialog-size';
import DialogDefinition from './dialog-definition';
import { instances } from './modal-view';
import dialogList from './modal-view-list';
import { Dialogs } from './namespace';

const defaultOptions = { size: DialogSize.DEFAULT };

const dfModal = {
  get isInstalled() { return instances.length > 0; },
  getDialogDefinition(existingDialog: number | Promise<any>) {
    if (existingDialog instanceof Promise) return dialogList.getDialogDefFromPromise(existingDialog);
    return dialogList.getDialogFromId(existingDialog);
  },
  fromRenderFunctions(existingDialog: number, dfDialog: DialogDefinition) {
    return dialogList.push(dfDialog, existingDialog);
  },
  fromFormDefinition(formDefinition: APIConsumer.FormDefinition) {
    const layout = formDefinition.layout;
    const payload = formDefinition.payload;
    const actions = formDefinition.actions;
    const actionHandlers = formDefinition.actionHandlers;
    const errors = formDefinition.errors;
    return this.message(
      formDefinition.title,
      {
        componentName: formDefinition.layout.componentName,
        props: { layout, payload, actions, errors },
      },
      actions.formFooter,
      { size: layout.size || DialogSize.DEFAULT },
      actionHandlers,
    );
  },
  message(
    title: Dialogs.DialogTitle,
    message: Dialogs.DialogMessage,
    actions?: FilteredActions,
    options?: Dialogs.DialogOptions,
    actionHandlers?: IHandlers,
  ) {
    if (actions) {
      // any actions that don't have special handlers, create the default handler that closes the dialog
      for (const action of actions) {
        const actionName = getActionName(action.name);
        if (!action[actionName]) action[actionName] = defaultActionHandler;
      }
    }
    const dialogDef = new DialogDefinition(
      title,
      message,
      options || defaultOptions,
      actions || new FilteredActions({ close: Action.closeAction({ actionClose: defaultActionHandler }) }),
      actionHandlers,
    );
    dialogList.push(dialogDef);
    return dialogDef.promise;
  },
  yesNo(
    title: Dialogs.DialogTitle,
    question: Dialogs.DialogMessage,
    actions?: FilteredActions,
    options?: Dialogs.DialogOptions,
  ) {
    const dialogDef = new DialogDefinition(
      title,
      question,
      options || defaultOptions,
      actions || new FilteredActions({
        yes: Action.yesAction({ actionYes: defaultActionHandler }),
        no: Action.noAction({ actionNo: defaultActionHandler }),
      }),
    );
    dialogList.push(dialogDef);
    return dialogDef.promise;
  },
};

export default dfModal;
