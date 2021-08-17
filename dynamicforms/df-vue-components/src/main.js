import Vue from 'vue';
import dftable from '@/components/dftable.vue';
import ModalHandler from '@/components/bootstrap/modalhandler.vue';
import VueObserveVisibility from 'vue-observe-visibility';
import axios from 'axios';
import $ from 'jquery';
import example from '@/examples/example.vue';

Vue.config.productionTip = false;
Vue.use(VueObserveVisibility);
Vue.component('dftable', dftable);
Vue.component('example', example);

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

const getComponentDef = (url, callback) => {
  axios
    .get(url, { headers: { 'x-viewmode': 'TABLE_ROW', 'x-pagination': 1, 'x-df-component-def': true } })
    .then((res) => { callback(res.data); })
    // eslint-disable-next-line no-alert
    .catch((err) => { alert(err.data); });
};

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
    components: { dftable, example },
  });
};

// This is exposed so that the base page template may use jQuery. Probably soon won't be needed
window.$ = $;
window.jQuery = window.$;

// Standard entry points to our Vue app. createApp initializes the Vue app and getComponentDef retrieves any definition
window.createApp = createApp;
window.getComponentDef = getComponentDef;
