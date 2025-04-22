import { find, findIndex } from 'lodash-es';
import { Ref, ref } from 'vue';

import FilteredActions from '../actions/filtered-actions';
import FormPayload from '../form/definitions/form-payload';

import DialogDefinition from './dialog-definition';

class DialogList {
  public list: DialogDefinition[];

  private currentRef: Ref<DialogDefinition | null>;

  constructor() {
    this.list = [];
    this.currentRef = ref(null);
  }

  setCurrent() {
    const newValue = this.list.length ? this.list[this.list.length - 1] : null;
    if (this.currentRef.value !== newValue) this.currentRef.value = newValue;
  }

  get current(): DialogDefinition | null {
    return this.currentRef.value;
  }

  push(dialogDef: DialogDefinition, existingDialogId?: number): number {
    const pos: number = findIndex(this.list, { dialogId: existingDialogId });

    if (pos !== -1) {
      // replace existing definition
      dialogDef.dialogId = <number>existingDialogId;
      this.list[pos] = dialogDef;
      if (pos === this.list.length - 1) dialogDef.topOfTheStack = true;
    } else {
      // add a new dialog to the top of the stack
      if (this.list.length) this.list[this.list.length - 1].topOfTheStack = false;
      if (dialogDef.actions instanceof FilteredActions) {
        const newPayload = FormPayload.create(dialogDef.actions.payload || FormPayload.create());
        newPayload.addExtraData({ dialog: dialogDef });
        dialogDef.actions = new FilteredActions(dialogDef.actions.actions, newPayload);
      }
      this.list.push(dialogDef);
      dialogDef.topOfTheStack = true;
    }
    const self = this;
    dialogDef.close = () => self.pop(dialogDef.dialogId);
    dialogDef.promise = new Promise((resolve, reject) => {
      dialogDef.resolvePromise = resolve;
      dialogDef.rejectPromise = reject;
    });
    this.setCurrent();
    return dialogDef.dialogId;
  }

  getDialogFromId(id: number) {
    const pos = findIndex(this.list, { dialogId: id });
    return pos !== -1 ? this.list[pos] : null;
  }

  pop(existingDialogId: number) {
    const pos = findIndex(this.list, { dialogId: existingDialogId });
    if (pos !== -1) {
      this.list.splice(pos, 1);
      if (this.list.length && pos === this.list.length) {
        this.list[this.list.length - 1].topOfTheStack = true;
      }
    }
    this.setCurrent();
  }

  isCurrentDialogPromise(promise: Promise<any>) {
    return this.current?.promise === promise;
  }

  getDialogDefFromPromise(promise: Promise<any>) {
    return find(this.list, { promise });
  }
}

const dialogList = new DialogList();

export { DialogDefinition };
export default dialogList;
