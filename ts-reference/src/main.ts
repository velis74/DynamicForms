import { createApp } from 'vue';

import App from './App.vue';
import router from './router';

import vuetify from "@/plugins/vuetify";
import VuetifyApp from '@/demo-app/vuetify-app.vue';
import VuetifyViewMode from '@/demo-app/view-mode.vue';
import TcolumnGeneric from '@/components/table/tcolumn-generic.vue';
import * as VuetifyComponents from '@/components/vuetify';

const app = createApp(App)

// globally defined components
app.component(VuetifyApp.name, VuetifyApp);
app.component(TcolumnGeneric.name, TcolumnGeneric);
app.component(VuetifyViewMode.name, VuetifyViewMode);
Object.values(VuetifyComponents).map((component) => app.component(component.name, component));

// add router
app.use(router);

// add vuetify
app.use(vuetify);

app.mount('#app')
