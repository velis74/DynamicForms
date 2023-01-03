import { defineComponent } from 'vue';

import DialogSize, { isDefined } from '@/components/classes/dialog-size';

import ModalRendererMixin from '@/components/modal/modal-renderer.mixin';

export default defineComponent({
  name: 'DfModal',
  mixins: [ModalRendererMixin],
  props: { // eslint-disable-line object-curly-newline
    value: { type: Boolean, required: true },
    size: { type: Number, default: () => DialogSize.DEFAULT, validator(value: number) { return isDefined(value); } },
  },
  data() {
    return {
      pushedDialog: null as any,
      topOfTheStack: false as boolean,
    };
  },
  render(el: any) {
    if (this.value) {
      // TODO: something here causes the DfModal component to rerender. This is triggered by simply creating
      //  the params object. If I only copied the $slots, everything would be fine. The problem now is that I get
      //  rerenders correctly when something changes in the using DOM, but incorrectly because I construct the params
      //  object new each time.
      //
      // The proper solution to the problem is to not attempt to circumvent Vue's rendering pipeline, but instead
      //  just properly detect which ONE dialog is at the top of the stack right now. And then render that one, hide
      //  all others
      this.pushedDialog = this.$dfModal.fromRenderFunctions(
        this.pushedDialog,
        {
          dialogComponent: this,
          isDfDialog: true,
          set topOfTheStack(value: boolean) { this.dialogComponent.topOfTheStack = value; },
        },
      );
      if (this.topOfTheStack) {
        return this.renderFunction(el, this.$slots.title, this.$slots.body, this.$slots.actions, { size: this.size });
      }
    } else if (this.pushedDialog) {
      this.$dfModal.popDialog(this.pushedDialog);
      this.pushedDialog = null;
    }
    return null;
  },
});
