<template>
  <component
    :is="themeComponent"
    :themes="themes"
    :examples="examples"
    :title="title"
    @theme-changed="(newTheme) => theme = newTheme"
  >
    <template #main-component>
      <router-view @title-change="setTitle"/>
    </template>
  </component>
</template>
<script>
import Vue from 'vue';
import VueRouter from 'vue-router';

import APIConsumerLoader from '../components/api_consumer/api_consumer_loader';

Vue.use(VueRouter);

const routes = [
  { title: 'Validated', path: '/validated', component: APIConsumerLoader },
  { title: 'Hidden fields', path: '/hidden-fields', component: APIConsumerLoader },
  { title: 'Basic fields', path: '/basic-fields', component: APIConsumerLoader },
  { title: 'Advanced fields', path: '/advanced-fields', component: APIConsumerLoader },
  { title: 'Page loading', path: '/page-load', component: APIConsumerLoader },
  { title: 'Filtering', path: '/filter', component: APIConsumerLoader },
  { title: 'Refresh types', path: '/refresh-types', component: APIConsumerLoader },
  { title: 'Custom CSS per row', path: '/calculated-css-class-for-table-row', component: APIConsumerLoader },
  // { path: '/single-dialog/:id', component: PageLoader, meta: { component: 'dialog', uuid: singleDlgFakeUUID } },
  // { path: '/choice-allow-tags-fields', component: PageLoader },
  // { path: '/calendar', component: Calendar },
  // { path: '/documents', component: PageLoader },
  // { path: '/view-mode', component: ViewMode },
];
const router = new VueRouter({ routes });

// import BootstrapApp from './bootstrap/bootstrap-app';
// import VuetifyApp from './vuetify/vuetify-app';

export default {
  name: 'DemoApp',
  router,
  components: {
    // eslint-disable-next-line import/extensions
    BootstrapApp: () => import('./bootstrap/bootstrap-app.vue'),
    // eslint-disable-next-line import/extensions
    VuetifyApp: () => import('./vuetify/vuetify-app.vue'),
  },
  data: () => ({
    title: '',
    theme: 'vuetify',
    themes: ['bootstrap', 'vuetify'],
  }),
  computed: {
    examples() {
      return routes.map((route) => ({ title: route.title, path: route.path }));
    },
    themeComponent() {
      switch (this.theme) {
      case 'bootstrap':
        return 'BootstrapApp';
      case 'vuetify':
        return 'VuetifyApp';
      default:
        throw new Error('Unknown theme');
      }
    },
  },
  methods: {
    setTitle(newTitle) {
      this.title = newTitle;
      document.title = `${newTitle} - DynamicForms`;
    },
  },
};
</script>
