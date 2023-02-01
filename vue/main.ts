import { createApp } from 'vue';

import DemoApp from './demo-app';
import dynamicForms from './plugins/dynamicForms';
import vuetify from './plugins/vuetify';
import router from './router';
import 'vuetify/styles/main.css';

const app = createApp(DemoApp);
app.use(router);
app.use(vuetify);
app.use(dynamicForms);

app.mount('#app');
