import Action from '../actions/action';
import FilteredActions from '../actions/filtered-actions';

import ModalViewList from './modal-view-list';

function createHandler(dialogDef) {
  const payloadVal = dialogDef?.body?.componentName ? dialogDef?.body?.props?.payload : null;
  return {
    handlerWithPayload: {
      handler: function handler(action, payload, extraData) {
        dialogDef.resolvePromise({ action, payload, extraData, dialog: dialogDef });
        dialogDef.close();
        return true;
      },
      payload: payloadVal,
      generated: true,
    },
  };
}

export default {
  mixins: [ModalViewList],
  methods: {
    fromRenderFunctions(existingDialog, dfDialog) {
      return this.pushDialog(dfDialog, existingDialog);
    },
    fromFormDefinition(formDefinition) {
      const layout = formDefinition.layout;
      const payload = formDefinition.payload;
      const actions = formDefinition.actions;
      return this.message(
        formDefinition.title,
        { componentName: formDefinition.layout.componentName, props: { layout, payload, actions, errors: {} } },
        formDefinition.actions.formFooter,
      );
    },
    message(title, message, actions, options) {
      const dialogDef = {
        title,
        body: message,
        options,
      };
      if (actions) {
        // any actions that don't have special handlers, create the default handler that closes the dialog
        for (const action of actions) {
          if (!action.handlerWithPayload || action.handlerWithPayload?.generated) {
            action.handlerWithPayload = createHandler(dialogDef).handlerWithPayload;
          }
        }
      }
      dialogDef.actions = actions || new FilteredActions([Action.closeAction(createHandler(dialogDef))]);
      this.pushDialog(dialogDef, null);
      return dialogDef.promise;
    },
    yesNo(title, question, actions, options) {
      const dialogDef = {
        title,
        body: question,
        options,
      };
      dialogDef.actions = new FilteredActions([
        Action.yesAction(createHandler(dialogDef)),
        Action.noAction(createHandler(dialogDef)),
      ]);
      this.pushDialog(dialogDef, null);
      return dialogDef.promise;
    },
  },
};
