import { ComponentPublicInstance, defineComponent, Slot } from 'vue';

import DialogSize from './definitions/dialog-size';
import DialogDefinition from './dialog-definition';
import ModalRenderer from './modal-renderer';
import dfModal from './modal-view-api';
import dialogList from './modal-view-list';

interface DfModalPublicInstance extends ComponentPublicInstance {
  topOfTheStack: boolean;
  size: number;
}

class DialogDefinitionWithSettableTop extends DialogDefinition {
  instance: DfModalPublicInstance;

  constructor(instance: DfModalPublicInstance) {
    // Jure 16.3.2023: types don't work here, but the code actually does.
    super(
      instance.$slots.title as Slot,
      instance.$slots.body as Slot,
      { size: instance.size },
      instance.$slots.actions as Slot,
    );
    this.instance = instance;
  }

  set topOfTheStack(value: boolean) {
    super.topOfTheStack = value;
    if (value !== this.instance.topOfTheStack) {
      console.log(`Top of the stack ${value}`);
      this.instance.topOfTheStack = value;
    }
  }
}

export default /* #__PURE__ */ defineComponent({
  name: 'DfDialog',
  mixins: [ModalRenderer],
  props: {
    modelValue: { type: Boolean, required: true },
    size: {
      type: Number,
      default: () => DialogSize.DEFAULT,
      validator(value: number) { return DialogSize.isDefined(value); },
    },
  },
  data() {
    return {
      pushedDialog: -1,
      topOfTheStack: false,
    };
  },
  render() {
    if (this.modelValue) {
      const topOfTheStack = this.topOfTheStack;

      if (this.pushedDialog <= 0 || dfModal.getDialogDefinition(this.pushedDialog)?.options.size !== this.size) {
        const pushedDialog = dfModal.fromRenderFunctions(this.pushedDialog, new DialogDefinitionWithSettableTop(this));
        if (pushedDialog !== this.pushedDialog) this.pushedDialog = pushedDialog;
      }
      if (topOfTheStack) {
        console.log('aha!', this.pushedDialog, this.modelValue, this.$slots.title, this.$slots);

        // return this.renderFunction(
        //   this.pushedDialog,
        //   'juhuhu', // this.$slots.title,
        //   this.$slots.default, // body
        //   this.$slots.actions,
        //   { size: this.size },
        // );
      }
    } else if (this.pushedDialog > 0) {
      dialogList.pop(this.pushedDialog);
      this.pushedDialog = -1;
    }
    return null;
  },
});
