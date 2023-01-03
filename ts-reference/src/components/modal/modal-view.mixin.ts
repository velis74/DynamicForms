import { defineComponent } from 'vue';

import requestTracker from '@/components/util/request-tracker';

import ModalRendererMixin from '@/components/modal/modal-renderer.mixin';
import ModalViewApiMixin from '@/components/modal/modal-view-api.mixin';

export default defineComponent({
  name: 'ModalView',
  mixins: [ModalRendererMixin, ModalViewApiMixin],
  data() {
    return { isPrimary: false as boolean };
  },
  created() { this.install(); },
  methods: {
    install() {
      const vue = this.$root;
      if (!vue?.modalRootInstance) {
        vue.modalRootInstance = this;
        this.isPrimary = true;
      }
      // TODO: HELP!!!!
      /*
      if (!Vue.prototype.$dfModal) {
        Object.defineProperty(Vue.prototype, '$dfModal', { get() { return this?.$root.modalRootInstance; } });
        requestTracker.dfModal = vue.modalRootInstance;
      }
       */
    },
    render(el: any) {
      const curDlg = this.currentDialog();
      if (this.isPrimary && curDlg && curDlg.isDfDialog === undefined) {
        return this.renderFunction(el, curDlg.title, curDlg.body, curDlg.actions, curDlg.options);
      }
      return null;
    },
  },
})
