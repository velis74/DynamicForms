import { defineComponent } from 'vue';

import Action from '@/components/actions/action';
import FilteredActions from '@/components/actions/filtered-actions';

import ModalViewListMixin from '@/components/modal/modal-view-list.mixin';
import type { DialogDefinition } from '@/components/modal/index';

function createHandler(dialogDef: any) {
  const payloadVal = dialogDef?.body?.componentName ? dialogDef?.body?.props?.payload : null;
  return {
    handlerWithPayload: {
      handler: (action: Action, payload: any, extraData: any): boolean => {
        dialogDef.resolvePromise({ action, payload, extraData, dialog: dialogDef });
        dialogDef.close();
        return true
      },
      payload: payloadVal,
    },
  };
}

export default defineComponent({
  mixins: [ModalViewListMixin],
  methods: {
    fromRenderFunctions(existingDialog: any, dfDialog: any) {
      return this.pushDialog(dfDialog, existingDialog);
    },
    fromFormDefinition(formDefinition: any) {
      const layout = formDefinition.layout;
      const payload = formDefinition.payload;
      const actions = formDefinition.actions;
      const errors = formDefinition.errors;
      return this.message(
        formDefinition.title,
        { componentName: formDefinition.layout.componentName, props: { layout, payload, actions, errors } },
        formDefinition.actions.formFooter,
      );
    },
    message(title: any, message: any, actions: any, options?: any) {
      const dialogDef = {
        title,
        body: message,
        options,
      } as DialogDefinition;
      if (actions) {
        // any actions that don't have special handlers, create the default handler that closes the dialog
        for (const action of actions) {
          if (!action.handlerWithPayload) {
            action.handlerWithPayload = createHandler(dialogDef).handlerWithPayload;
          }
        }
      }
      dialogDef.actions = actions || new FilteredActions([Action.closeAction(createHandler(dialogDef))]);
      this.pushDialog(dialogDef, null);
      return dialogDef.promise;
    },
  }
});
