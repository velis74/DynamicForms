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

      <template #append>
        <v-menu bottom right close-on-click offset-y>
          <template #activator="{ props }">
            <v-btn dark text color="light" v-bind="props"><span>Theme</span></v-btn>
          </template>
          <v-list>
            <v-list-item v-for="theme in themes" :key="theme" @click="$emit('theme-changed', theme)">
              <div class="text-button">{{ theme }}</div>
            </v-list-item>
          </v-list>
        </v-menu>
      </template>
    </v-app-bar>

    <v-navigation-drawer v-model="drawer" absolute temporary>
      <v-list nav>
        <v-list-item v-for="example in examples" :key="example.title" :to="example.path">
          <v-list-item-title>{{ example.title }}</v-list-item-title>
        </v-list-item>
      </v-list>
    </v-navigation-drawer>

    <v-main>
      <ModalView/>
      <slot name="main-component"/>
    </v-main>
  </v-app>
</template>

<script lang="ts">
import { defineComponent } from 'vue';

export default /* #__PURE__ */ defineComponent({
  name: 'VuetifyApp',
  props: {
    title: { type: String, required: true },
    themes: { type: Array, required: true },
    examples: { type: Array, required: true },
  },
  emits: ['theme-changed'],
  data: () => ({ drawer: false }),
});
</script>
