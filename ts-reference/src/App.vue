<script setup lang="ts">
import { RouterView } from 'vue-router'
</script>

<template>
  <component
    :is="themeComponent"
    :themes="themes"
    :examples="examples"
    :title="title"
    @theme-changed="changeTheme"
  >
    <template v-slot:main-component>
      <RouterView @title-change="setTitle"/>
    </template>
  </component>
</template>

<script lang="ts">
import _ from 'lodash';
import { defineComponent } from 'vue';

import routes from '@/routes';

export default defineComponent({
  name:'DemoApp',
  data: () => ({
    title: '',
    theme: localStorage.getItem('df-theme') && localStorage.getItem('df-theme') !== 'undefined' ?
      localStorage.getItem('df-theme') : 'vuetify',
    themes: ['bootstrap', 'vuetify'],
    themeData: {
      bootstrap: [],
      vuetify: [],
    } as any,
  }),
  computed: {
    examples() {
      return routes.map((route) => ({ title: route.meta.title, path: route.path }));
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
    }
  },
  mounted() { this.resetResources(null); },
  methods: {
    setTitle(newTitle: string) {
      this.title = newTitle;
    },
    removeResources(theme: string) {
      const removed: any[] = [];
      _.forEach(Array.prototype.slice.call(document.getElementsByTagName('link')).concat(
        Array.prototype.slice.call(document.getElementsByTagName('script')),
      ), (s: any) => {
        if ((s.href && _.includes(s.href, `.${theme}.css`)) ||
            (s.src && _.includes(s.src, `.${theme}.js`)) ||
            (s.href && _.includes(s.href, `.${theme}.js`))) {
          document.getElementsByTagName('head')[0].removeChild(s);
          removed.push(s);
        }
      });
      return removed;
    },
    resetResources(newTheme: string | null) {
      if (!newTheme) {
        _.forEach(_.filter(this.themes, (t: string) => t !== this.theme), (th: string) => {
          this.removeResources(th);
        });
        return;
      }
      if (this.theme) {
        const removedResources = this.removeResources(this.theme);
        if (!_.size(this.themeData[this.theme])) {
          this.themeData[this.theme] = this.themeData[this.theme].concat(removedResources);
        }
        _.forEach(this.themeData[newTheme], (v: any) => {
          document.getElementsByTagName('head')[0].appendChild(v);
        });
      }
    },
    changeTheme(newTheme: string) {
      localStorage.setItem('df-theme', newTheme);
      if (newTheme !== this.theme) {
        this.resetResources(newTheme);
        this.theme = newTheme;
      }
    }
  },
});
</script>
