import DialogSize from '../classes/dialog_size';

export default {
  name: 'Modal',
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
    if (this.value) {
      // TODO: For some reason Vue thinks this creates an infinite update loop vs passing just this.$slots
      const params = {
        title: this.$slots.title,
        body: this.$slots.body,
        actions: this.$slots.actions,
        options: { size: this.size },
      };
      this.pushedDialog = this.$dfModal.fromRenderFunctions(this.pushedDialog, params);
      return null;
    }
    this.pushedDialog = null;
    return null;
  },
};
