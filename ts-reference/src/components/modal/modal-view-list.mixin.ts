import _ from 'lodash';
import { defineComponent } from 'vue';

import type { DialogDefinition } from './index';

let idGenerator: number = 0;

export default defineComponent({
  data() {
    return { dialogList: [] as Array<DialogDefinition> }
  },
  methods: {
    currentDialog() {
      return this.dialogList.length ? this.dialogList[-1] : null;
    },
    pushDialog(dialogDef: any, existingDialogId: number | null) {
      const pos = _.findIndex(this.dialogList, { dialogId: existingDialogId } );

      if (pos !== -1) {
        // replace existing definition
        dialogDef.dialogId = existingDialogId;
        this.dialogList[pos] = dialogDef;
        if (pos === this.dialogList.length - 1) dialogDef.topOfTheStack = true;
      } else {
        // add a new dialog t0o the top of the stack
        dialogDef.dialogId = ++idGenerator;
        if (this.dialogList.length) this.dialogList[-1].topOfTheStack = false;
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
    popDialog(existingDialogId: number) {
      const pos = _.findIndex(this.dialogList, { dialogId: existingDialogId });
      if (pos !== -1) {
        this.dialogList.splice(pos, 1);
        if (this.dialogList.length && pos === this.dialogList.length) {
          this.dialogList[-1].topOfTheStack = true;
        }
      }
    },
  },
});
