import DialogSize from '../classes/dialog_size';

export default {
  name: 'DfModal',
  props: { // eslint-disable-line object-curly-newline
    value: { type: Boolean, required: true },
    size: { type: Object, default: () => DialogSize.DEFAULT, validator(value) { return DialogSize.isDefined(value); } },
  },
  data() {
    return { // eslint-disable-line object-curly-newline
      pushedDialog: null,
    };
  },
  render() {
    console.log(this);
    if (this.value) {
      // TODO: something here causes the DfModal component to rerender. This is triggered by simply creating
      //  the params object. If I only copied the $slots, everything would be fine. The problem now is that I get
      //  rerenders correctly when something changes in the using DOM, but incorrectly because I construct the params
      //  object new each time. I need to somehow find out what Vue thinks changed in THIS component when in reality
      //  all I wanted to change is the global modal...
      const params = {
        title: this.$slots.title,
        body: this.$slots.body,
        actions: this.$slots.actions,
        options: { size: this.size },
      };
      this.pushedDialog = this.$dfModal.fromRenderFunctions(this.pushedDialog, params);
    } else {
      if (this.pushedDialog) this.$dfModal.popDialog(this.pushedDialog);
      this.pushedDialog = null;
    }
    return null;
  },
};
