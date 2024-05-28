<template>
  <vuetify-app
    :examples="examples"
    :title="title"
  >
    <template #main-component>
      <router-view @title-change="setTitle"/>
    </template>
  </vuetify-app>
</template>

<script lang="ts">
import { defineComponent } from 'vue';

import routes from '../routes';

import VuetifyApp from './vuetify/vuetify-app.vue';

export default defineComponent({
  name: 'DemoApp',
  components: { VuetifyApp },
  data: () => ({ title: '' }),
  computed: {
    examples() {
      return routes.map((route) => ({ title: route.meta.title, path: route.path }));
    },
  },
  methods: {
    setTitle(newTitle: string) {
      this.title = newTitle;
      document.title = `${newTitle} - DynamicForms`;
    },
  },
});
</script>
