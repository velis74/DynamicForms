<script setup lang="ts">
import { DfApp } from 'dynamicforms';
import { ref } from 'vue';

defineProps<{
  title: string,
  themes: string[],
  examples: { title: string, path: string }[]
}>();

defineEmits(['theme-changed']);

const drawer = ref<boolean>(false);
</script>

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
            <v-btn dark color="light" v-bind="props"><span>Theme</span></v-btn>
          </template>
          <v-list>
            <v-list-item v-for="theme in themes" :key="theme" @click="$emit('theme-changed', theme)">
              <div class="text-button">{{ theme }}</div>
            </v-list-item>
          </v-list>
        </v-menu>
      </template>
    </v-app-bar>

    <v-navigation-drawer v-model="drawer" temporary>
      <v-list nav>
        <v-list-item v-for="example in examples" :key="example.title" :to="example.path">
          <v-list-item-title>{{ example.title }}</v-list-item-title>
        </v-list-item>
      </v-list>
    </v-navigation-drawer>

    <v-main>
      <df-app>
        <slot name="main-component"/>
      </df-app>
    </v-main>
  </v-app>
</template>
