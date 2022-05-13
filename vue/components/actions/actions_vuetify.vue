<template>
  <div v-if="actions != null && actions.length > 0">
    <v-btn
      v-for="(action,idx) in actions"
      :key="idx"
      :elevation="0"
    >
      <IonIcon v-if="action.displayIcon" class="action-icon" :name="action.icon"/>
      <span v-if="showMargin(action)" style="width: .5rem"/>
      <span v-if="action.displayLabel">{{ action.labelText }}</span>
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
