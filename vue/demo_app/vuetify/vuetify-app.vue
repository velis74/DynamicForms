<template>
  <v-app>
    <v-app-bar app color="primary" dark>
      <v-app-bar-nav-icon variant="text" @click.stop="drawer = !drawer"/>

      <div class="d-flex align-center">
        <!--v-img
          alt="Vuetify Logo"
          class="shrink mr-2"
          contain
          src="https://cdn.vuetifyjs.com/images/logos/vuetify-logo-dark.png"
          transition="scale-transition"
          width="40"
        /-->
        <h2>DynamicForms{{ title ? ` - ${title}` : '' }}</h2>
      </div>

      <v-spacer/>

      <v-menu bottom right close-on-click offset-y>
        <template #activator="{ on, attrs }">
          <v-btn dark text color="light" v-bind="attrs" v-on="on"><span>Theme</span></v-btn>
        </template>
        <v-list>
          <v-list-item v-for="theme in themes" :key="theme" @click="$emit('theme-changed', theme)">
            <div class="text-button">{{ theme }}</div>
          </v-list-item>
        </v-list>
      </v-menu>
    </v-app-bar>

    <v-navigation-drawer v-model="drawer" absolute temporary>
      <v-list nav>
        <v-list-item v-for="example in examples" :key="example.title" :to="example.path">
          <v-list-item-title>{{ example.title }}</v-list-item-title>
        </v-list-item>
      </v-list>
    </v-navigation-drawer>

    <v-main>
      <slot name="main-component"/>
    </v-main>
  </v-app>
</template>

<script>
import Vue from 'vue';

import * as VuetifyComponents from '../../components/vuetify';

import vuetify from './vuetify';

Object.values(VuetifyComponents).map((component) => Vue.component(component.name, component));

export default {
  name: 'VuetifyApp',
  vuetify,
  props: {
    title: { type: String, required: true },
    themes: { type: Array, required: true },
    examples: { type: Array, required: true },
  },
  emits: ['theme-changed'],
  data: () => ({ drawer: false }),
};
</script>
