import _ from 'lodash';

import FilteredActions from '../actions/filtered-actions';

let idGenerator = 0;

export default {
  data() {
    return {
      dialogList: [],
      // actions is declared so that the action-handler-mixin stops looking for action executors here
      //  this way actions declared with modal-view-api are executed here and only here
      //  if we didn't do this, declaring actionXxx handler anywhere above here would result in that handler being used
      // TODO: the entire concept of action handlers might be a bit counterintuitive since we're not specifying
      //  precise handlers for precise actions. Instead we just declare a handler which might get called for an action
      //  it knows nothing about (except that it has the same name).
      actions: new FilteredActions([]),
    };
  },
  methods: {
    currentDialog() {
      return this.dialogList.length ? this.dialogList[this.dialogList.length - 1] : null;
    },
    pushDialog(dialogDef, existingDialogId) {
      const pos = _.findIndex(this.dialogList, { dialogId: existingDialogId });

      if (pos !== -1) {
        // replace existing definition
        dialogDef.dialogId = existingDialogId;
        this.dialogList[pos] = dialogDef;
        if (pos === this.dialogList.length - 1) dialogDef.topOfTheStack = true;
      } else {
        // add a new dialog to the top of the stack
        dialogDef.dialogId = ++idGenerator;
        if (this.dialogList.length) this.dialogList[this.dialogList.length - 1].topOfTheStack = false;
        this.dialogList.push(dialogDef);
        dialogDef.topOfTheStack = true;
      }
      const self = this;
      dialogDef.close = () => self.popDialog(dialogDef.dialogId);
      const promise = {};
      promise.promise = new Promise((resolve, reject) => {
        promise.resolve = resolve;
        promise.reject = reject;
      });
      dialogDef.promise = promise;
      return dialogDef.dialogId;
    },
    popDialog(existingDialogId) {
      const pos = _.findIndex(this.dialogList, { dialogId: existingDialogId });
      if (pos !== -1) {
        this.dialogList.splice(pos, 1);
        if (this.dialogList.length && pos === this.dialogList.length) {
          this.dialogList[this.dialogList.length - 1].topOfTheStack = true;
        }
      }
    },
    processActionsGeneric(action, payload, extraData) {
      if (this.dialogList.length) {
        const currentDialogDef = this.dialogList[this.dialogList.length - 1];
        currentDialogDef.promise.resolve({ action, payload, extraData, dialog: currentDialogDef });
        currentDialogDef.close();
        return true;
      }
      return false;
    },
  },
};
