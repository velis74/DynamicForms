import { createApp } from 'vue';
import { createVuetify, ThemeDefinition } from 'vuetify/dist/vuetify';
import 'vuetify/styles/main.css';

import GenericColumn from './components/table/tcolumn-generic.vue';
import * as VuetifyComponents from './components/vuetify';
import DemoApp from './demo-app';
import VuetifyViewMode from './demo-app/vuetify/view-mode.vue';
import VuetifyApp from './demo-app/vuetify/vuetify-app.vue';
import router from './router';

const app = createApp(DemoApp);

// vuetify components
app.component(VuetifyApp.name, VuetifyApp);
app.component(VuetifyViewMode.name, VuetifyViewMode);
Object.values(VuetifyComponents).map((component) => app.component(component.name, component));

app.component(GenericColumn.name, GenericColumn);

app.use(router);

const defaultTheme: ThemeDefinition = {
  dark: false,
  colors: {
    background: '#f8f8f8',
    surface: '#ffffff',
    // 'primary-darken-1': '#3700B3',
    // 'secondary-darken-1': '#018786',
    primary: '#3f51b5',
    secondary: '#2196f3',
    accent: '#ffc107',
    error: '#f44336',
    warning: '#ff9800',
    info: '#8bc34a',
    success: '#00bcd4',
  },
};

const vuetify = createVuetify({ theme: { defaultTheme: 'defaultTheme', themes: { defaultTheme } } });
app.use(vuetify);

app.mount('#app');
