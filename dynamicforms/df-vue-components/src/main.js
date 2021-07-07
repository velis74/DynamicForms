import Vue from 'vue';
import dftable from '@/components/dftable.vue';
import ModalHandler from '@/components/bootstrap/modalhandler.vue';
import VueObserveVisibility from 'vue-observe-visibility';

Vue.config.productionTip = false;
Vue.use(VueObserveVisibility);
Vue.component('dftable', dftable);

// const createTable = (elementId, configuration) => new Vue({
//   render: (h) => h(Table, {
//     props: {
//       configuration,
//     },
//   }),
// }).$mount(`#${elementId}`);

const createModal = (elementId) => new Vue({
  el: `#${elementId}`,
  components: { ModalHandler },
  template: '<ModalHandler></ModalHandler>',
});

const createApp = (elementId, template, props, modalId = null) => {
  if (typeof window.dynamicforms === 'undefined') {
    window.dynamicforms = {};
  }
  if (!window.dynamicforms.dialog && modalId) {
    createModal(modalId);
  }
  return new Vue({
    el: `#${elementId}`,
    template,
    data() {
      return props;
    },
    components: { dftable },
  });
};

window.createApp = createApp;
