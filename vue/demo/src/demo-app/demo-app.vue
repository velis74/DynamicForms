<template>
  <!-- @theme-changed="changeTheme"-->
  <vuetify-app
    :themes="themes"
    :examples="examples"
    :title="title"
  >
    <template #main-component>
      <router-view @title-change="setTitle"/>
    </template>
  </vuetify-app>
</template>

<script lang="ts">
/**
 * TODO: not all demos working yet. must port more from the old ViewMode
 * TODO: unit tests for everything. none there yet
 */
import { defineComponent } from 'vue';

import routes from '../routes';

import VuetifyApp from './vuetify/vuetify-app.vue';

export default /* #__PURE__ */ defineComponent({
  name: 'DemoApp',
  components: { VuetifyApp },
  data: () => ({
    title: '',
    // eslint-disable-next-line max-len
    theme: localStorage.getItem('df-theme') && localStorage.getItem('df-theme') !== 'undefined' ?
      localStorage.getItem('df-theme') : 'vuetify',
    themes: ['bootstrap', 'vuetify'],
    themeData: {
      bootstrap: [],
      vuetify: [],
    },
  }),
  computed: {
    examples() {
      return routes.map((route) => ({ title: route.meta.title, path: route.path }));
    },
  },
  /*
  mounted() {
    this.resetResources(null);
  },
  */
  methods: {
    setTitle(newTitle: string) {
      this.title = newTitle;
      document.title = `${newTitle} - DynamicForms`;
    },
    /*
    removeResources(theme) {
      const removed = [];
      _.forEach(Array.prototype.slice.call(document.getElementsByTagName('link')).concat(
        Array.prototype.slice.call(document.getElementsByTagName('script')),
      ), (s) => {
        if ((s.href && _.includes(s.href, `.${theme}.css`)) ||
          (s.src && _.includes(s.src, `.${theme}.js`)) ||
          (s.href && _.includes(s.href, `.${theme}.js`))) {
          document.getElementsByTagName('head')[0].removeChild(s);
          removed.push(s);
        }
      });
      return removed;
    },
    resetResources(newTheme) {
      if (!newTheme) {
        _.forEach(_.filter(this.themes, (t) => t !== this.theme), (th) => {
          this.removeResources(th);
        });
        return;
      }
      const removedResources = this.removeResources(this.theme);
      if (!_.size(this.themeData[this.theme])) {
        this.themeData[this.theme] = this.themeData[this.theme].concat(removedResources);
      }
      _.forEach(this.themeData[newTheme], (v) => {
        document.getElementsByTagName('head')[0].appendChild(v);
      });
    },
    changeTheme(newTheme) {
      localStorage.setItem('df-theme', newTheme);
      if (newTheme !== this.theme) {
        this.resetResources(newTheme);
        this.theme = newTheme;
      }
    },
    */
  },
});
</script>
