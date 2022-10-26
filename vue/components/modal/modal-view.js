import Vue from 'vue';

import requestTracker from '../util/request-tracker';

import ModalRenderer from './modal-renderer';
import ModalViewAPI from './modal-view-api';

export default {
  name: 'ModalView',
  mixins: [ModalRenderer, ModalViewAPI],
  data() {
    return { // eslint-disable-line object-curly-newline
      isPrimary: false,
    };
  },
  created() { this.install(); },
  methods: {
    install() {
      const vue = this.$root;
      if (!vue.modalRootInstance) {
        vue.modalRootInstance = this;
        this.isPrimary = true;
      }
      if (!Vue.prototype.$dfModal) {
        Object.defineProperty(Vue.prototype, '$dfModal', { get() { return this?.$root.modalRootInstance; } });
        requestTracker.dfModal = vue.modalRootInstance;
      }
    },
  },
  render(el) {
    const curDlg = this.currentDialog();
    if (this.isPrimary && curDlg && curDlg.isDfDialog === undefined) {
      return this.renderFunction(el, curDlg.title, curDlg.body, curDlg.actions, curDlg.options);
    }
    return null;
  },
};
