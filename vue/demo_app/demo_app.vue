<template>
  <component
    :is="themeComponent"
    :themes="themes"
    :examples="examples"
    @theme-changed="(newTheme) => theme = newTheme"
  />
</template>
<script>
import Vue from 'vue';
import VueRouter from 'vue-router';

import BootstrapApp from './bootstrap/bootstrap-app';
import VuetifyApp from './vuetify/vuetify-app';

Vue.use(VueRouter);

const routes = [
  { title: 'Validated', path: '/validated' }, // , component: PageLoader },
  // { path: '/hidden-fields', component: PageLoader },
  // { path: '/basic-fields', component: PageLoader },
  // { path: '/advanced-fields', component: PageLoader },
  // { path: '/page-load', component: PageLoader },
  // { path: '/filter', component: PageLoader },
  // { path: '/refresh-types', component: PageLoader },
  // { path: '/calculated-css-class-for-table-row', component: PageLoader },
  // { path: '/single-dialog/:id', component: PageLoader, meta: { component: 'dialog', uuid: singleDlgFakeUUID } },
  // { path: '/choice-allow-tags-fields', component: PageLoader },
  // { path: '/calendar', component: Calendar },
  // { path: '/documents', component: PageLoader },
  // { path: '/view-mode', component: ViewMode },
];
const router = new VueRouter({ routes });

export default {
  name: 'DemoApp',
  router,
  components: { VuetifyApp, BootstrapApp },
  data: () => ({
    theme: 'material',
    themes: ['bootstrap', 'material'],
  }),
  computed: {
    examples() {
      return routes.map((route) => ({ title: route.title, path: route.path }));
    },
    themeComponent() {
      switch (this.theme) {
      case 'bootstrap':
        return 'BootstrapApp';
      case 'material':
        return 'VuetifyApp';
      default:
        throw new Error('Unknown theme');
      }
    },
  },
};
</script>
