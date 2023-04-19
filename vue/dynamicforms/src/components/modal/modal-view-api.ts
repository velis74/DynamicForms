import Action, { defaultActionHandler, getActionName } from '../actions/action';
import FilteredActions from '../actions/filtered-actions';

import DialogDefinition from './dialog-definition';
import DialogSize from './dialog-size';
import { instances } from './modal-view';
import dialogList from './modal-view-list';

import DialogMessage = Dialogs.DialogMessage;
import DialogOptions = Dialogs.DialogOptions;
import DialogTitle = Dialogs.DialogTitle;

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
    const errors = formDefinition.errors;
    return this.message(
      formDefinition.title,
      { componentName: formDefinition.layout.componentName, props: { layout, payload, actions, errors } },
      actions.formFooter,
    );
  },
  message(title: DialogTitle, message: DialogMessage, actions?: FilteredActions, options?: DialogOptions) {
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
      actions || new FilteredActions([Action.closeAction({ actionClose: defaultActionHandler })]),
    );
    dialogList.push(dialogDef);
    return dialogDef.promise;
  },
  yesNo(title: DialogTitle, question: DialogMessage, actions?: FilteredActions, options?: DialogOptions) {
    const dialogDef = new DialogDefinition(
      title,
      question,
      options || defaultOptions,
      actions || new FilteredActions([
        Action.yesAction({ actionYes: defaultActionHandler }),
        Action.noAction({ actionNo: defaultActionHandler }),
      ]),
    );
    dialogList.push(dialogDef);
    return dialogDef.promise;
  },
};

export default dfModal;