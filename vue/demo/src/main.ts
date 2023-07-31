import { createApp } from 'vue';

import DemoApp from './demo-app';
import ExampleHiddenLayout from './demo-app/example-hidden-layout.vue';
import ViewMode from './demo-app/vuetify/view-mode.vue';
import VuetifyApp from './demo-app/vuetify/vuetify-app.vue';
import dynamicForms from './plugins/dynamicForms';
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
app.component(ViewMode.name, ViewMode);
app.component(ExampleHiddenLayout.name, ExampleHiddenLayout);

app.mount('#app');
