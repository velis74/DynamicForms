<template>
  <div v-if="actions != null && actions.length > 0">
    <v-btn
      v-for="action in actions"
      :key="action.name + action.icon"
      :text="asText(action)"
      :icon="asIcon(action)"
      :x-small="true"
      :elevation="0"
    >
      <IonIcon v-if="showIcon(action)" class="action-icon" :name="action.icon"/>
      <span v-if="showMargin(action)" style="width: .5rem"/>
      <span v-if="showLabel(action)">{{ action.label }}</span>
    </v-btn>
  </div>
</template>

<script>
import IonIcon from 'vue-ionicon';

import Actions from './actions';

export default {
  name: 'VuetifyActions',
  components: { IonIcon },
  mixins: [Actions],
  methods: {
    asText(action) {
      return !this.displayStyle[action.name].asButton;
    },
    asIcon(action) {
      return !this.showLabel(action);
    },
    showIcon(action) {
      return this.displayStyle[action.name].showIcon;
    },
    showMargin(action) {
      return this.showIcon(action) && this.showLabel(action);
    },
    showLabel(action) {
      return this.displayStyle[action.name].showLabel;
    },
  },
};
</script>

<style scoped>
  @import "actions.css";
</style>
