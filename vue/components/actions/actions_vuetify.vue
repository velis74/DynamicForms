<template>
  <div v-if="actions != null && actions.length > 0">
    <v-btn
      v-for="(action,idx) in actions"
      :key="idx"
      :elevation="0"
    >
      <IonIcon v-if="displayIcon(action)" class="action-icon" :name="action.icon"/>
      <span v-if="displayIcon(action) && displayLabel(action)" style="width: .5rem"/>
      <span v-if="displayLabel(action)">{{ labelText(action) }}</span>
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
};
</script>

<style scoped>
  @import "actions.css";
</style>
