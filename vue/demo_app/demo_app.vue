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
/**
 * TODO: not all demos working yet. must port more from the old ViewMode
 * TODO: unit tests for everything. none there yet
 */
import Vue from 'vue';
import VueRouter from 'vue-router';

import APIConsumerLoader from '../components/api_consumer/api_consumer_loader';
import * as BootstrapComponents from '../components/bootstrap';
import * as VuetifyComponents from '../components/vuetify';

import BootstrapApp from './bootstrap/bootstrap-app';
import NamedComponentLoader from './named_component_loader';
import VuetifyApp from './vuetify/vuetify-app';

Vue.use(VueRouter);
Object.values(VuetifyComponents).map((component) => Vue.component(component.name, component));
Object.values(BootstrapComponents).map((component) => Vue.component(component.name, component));

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
  {
    title: 'The three view-modes',
    path: '/view-mode',
    component: NamedComponentLoader,
    props: { componentName: 'ViewMode', componentNameAddTemplateName: true, componentProps: {} },
  },
];
const router = new VueRouter({ routes });

export default {
  name: 'DemoApp',
  router,
  components: { VuetifyApp, BootstrapApp },
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
