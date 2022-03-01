import { BootstrapVue } from 'bootstrap-vue';
import Vue from 'vue';

import DemoApp from './demo_app';
import vuetify from './demo_app/vuetify/vuetify';

import 'bootstrap/dist/css/bootstrap.css';
import 'bootstrap-vue/dist/bootstrap-vue.css';

Vue.config.productionTip = false;
Vue.use(BootstrapVue);

new Vue({
  vuetify,
  el: '#app',
  components: { DemoApp },
  render: (r) => r(DemoApp),
}).$mount('body');
