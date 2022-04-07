export default {
  name: 'Modal',
  props: { // eslint-disable-line object-curly-newline
    value: { type: Boolean, required: true },
  },
  data() {
    return { // eslint-disable-line object-curly-newline
      pushedDialog: null,
    };
  },
  render(el) {
    if (this.value) {
      this.pushedDialog = this.$dfModal.fromRenderFunctions(this.pushedDialog, this.$slots);
      return el('p', 'test');
    }
    this.pushedDialog = null;
    return null;
  },
};
