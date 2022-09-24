<template>
  <b-modal v-model="doShow" :size="computedClass">
    <template #modal-title>
      <slot name="title"/>
    </template>
    <slot name="body"/>
    <template #modal-footer>
      <slot name="actions"/>
    </template>
  </b-modal>
</template>

<script>
import DialogSize from '../classes/dialog-size';

export default {
  name: 'BootstrapModal',
  props: {
    show: { type: Boolean, default: () => false },
    options: { type: Object, required: true },
  },
  data() {
    return { doShow: this.show, fullScreen: false };
  },
  computed: {
    size() {
      return this.options.size;
    },
    computedClass() {
      console.log(this.size, 66, !this.fullScreen, DialogSize.SMALL);
      if (!this.fullScreen) {
        switch (this.size) {
        case DialogSize.SMALL:
          return 'sm';
        case DialogSize.LARGE:
          return 'lg';
        case DialogSize.X_LARGE:
          return 'xl';
        default:
          return '';
        }
      }
      return '';
    },
  },
};
</script>
