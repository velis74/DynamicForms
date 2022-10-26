import _ from 'lodash';

let idGenerator = 0;

export default {
  data() {
    return { dialogList: [] };
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
      dialogDef.promise = new Promise((resolve, reject) => {
        dialogDef.resolvePromise = resolve;
        dialogDef.rejectPromise = reject;
      });
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
    isCurrentDialogPromise(promise) {
      return this.currentDialog() && this.currentDialog().promise == promise;
    },
    getDialogDefFromPromise(promise) {
      return _.find(this.dialogList, { promise });
    },
  },
};
