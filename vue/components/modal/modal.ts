import { ComponentPublicInstance, defineComponent } from 'vue';

import DialogDefinition from './dialog-definition';
import DialogSize from './dialog-size';
import ModalRenderer from './modal-renderer';
import dfModal from './modal-view-api';
import dialogList from './modal-view-list';

class DialogDefinitionWithSettableTop extends DialogDefinition {
  instance: ComponentPublicInstance;

  constructor(instance: ComponentPublicInstance) {
    super(instance.$slots.title, instance.$slots.body, { size: instance.size }, instance.$slots.actions);
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
  name: 'DfModal',
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
