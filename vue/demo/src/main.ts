import { createApp } from 'vue';

import DemoApp from './demo-app';
import DfViewMode from './demo-app/vuetify/view-mode.vue';
import VuetifyApp from './demo-app/vuetify/vuetify-app.vue';
import dynamicForms from './plugins/dynamic-forms';
import vuetify from './plugins/vuetify';
import router from './router';

import 'vuetify/styles/main.css';
// eslint-disable-next-line import/no-relative-packages
import '../../dynamicforms/dist/style.css';

const app = createApp(DemoApp);
app.use(router);
app.use(vuetify);
app.use(dynamicForms);

// demo specific components
app.component('DfApp', VuetifyApp);
app.component('DfViewMode', DfViewMode);

app.mount('#app');
