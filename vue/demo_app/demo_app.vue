<template>
  <component
    :is="themeComponent"
    :themes="themes"
    :examples="examples"
    :title="title"
    @theme-changed="changeTheme"
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
import _ from 'lodash';
import Vue from 'vue';
import VueRouter from 'vue-router';

import APIConsumerLoader from '../components/api_consumer/api_consumer_loader';

import NamedComponentLoader from './named_component_loader';

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
  components: {
    // eslint-disable-next-line import/extensions
    BootstrapApp: () => import(/* webpackChunkName: "bootstrap" */ './bootstrap/bootstrap-app.vue'),
    // eslint-disable-next-line import/extensions
    VuetifyApp: () => import(/* webpackChunkName: "vuetify" */ './vuetify/vuetify-app.vue'),
  },
  data: () => ({
    title: '',
    // eslint-disable-next-line max-len
    theme: localStorage.getItem('df-theme') && localStorage.getItem('df-theme') !== 'undefined' ? localStorage.getItem('df-theme') : 'vuetify',
    themes: ['bootstrap', 'vuetify'],
    themeData: {
      bootstrap: [],
      vuetify: [],
    },
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
    changeTheme(newTheme) {
      localStorage.setItem('df-theme', newTheme);
      if (newTheme !== this.theme) {
        const saveOldData = !_.size(this.themeData[this.theme]);
        _.forEach(Array.prototype.slice.call(document.getElementsByTagName('link')).concat(
          Array.prototype.slice.call(document.getElementsByTagName('script')),
        ), (s) => {
          if ((s.href && _.includes(s.href, `.${this.theme}.css`)) ||
              (s.src && _.includes(s.src, `.${this.theme}.js`)) ||
              (s.href && _.includes(s.href, `.${this.theme}.js`))) {
            document.getElementsByTagName('head')[0].removeChild(s);
            if (saveOldData) {
              this.themeData[this.theme].push(s);
            }
          }
        });
        _.forEach(this.themeData[newTheme], (v) => {
          document.getElementsByTagName('head')[0].appendChild(v);
        });
        this.theme = newTheme;
      }
    },
  },
};
</script>
