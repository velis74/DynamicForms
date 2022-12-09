import { createApp } from 'vue';
import { createVuetify } from 'vuetify/dist/vuetify';
import 'vuetify/styles';

import GenericColumn from './components/table/tcolumn-generic';
import * as VuetifyComponents from './components/vuetify';
import DemoApp from './demo-app';
import VuetifyViewMode from './demo-app/vuetify/view-mode';
import VuetifyApp from './demo-app/vuetify/vuetify-app';
import router from './router';

const app = createApp(DemoApp);

// vuetify components
app.component(VuetifyApp.name, VuetifyApp);
app.component(VuetifyViewMode.name, VuetifyViewMode);
Object.values(VuetifyComponents).map((component) => app.component(component.name, component));

app.component(GenericColumn.name, GenericColumn);

app.use(router);

const vuetify = createVuetify({});
app.use(vuetify);

app.mount('#app');
