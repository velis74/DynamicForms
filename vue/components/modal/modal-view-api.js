import Action from '../actions/action';
import FilteredActions from '../actions/filtered-actions';

import ModalViewList from './modal-view-list';

export default {
  mixins: [ModalViewList],
  methods: {
    fromRenderFunctions(existingDialog, dfDialog) {
      return this.pushDialog(dfDialog, existingDialog);
    },
    message(title, message, actions, options) {
      const dialogDef = {
        title,
        body: message,
        actions: actions || new FilteredActions([Action.closeAction()]),
        options,
      };
      this.pushDialog(dialogDef, null);
      return dialogDef.promise.promise;
    },
    yesNo(title, question, actions, options) {
      const dialogDef = {
        title,
        body: question,
        actions: new FilteredActions([Action.yesAction(), Action.noAction()]),
        options,
      };
      this.pushDialog(dialogDef, null);
      return dialogDef.promise.promise;
    },
  },
};
