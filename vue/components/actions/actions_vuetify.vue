<template>
  <v-row v-if="actions != null && actions.length > 0" align="end" justify="end">
    <v-btn
      v-for="(action,idx) in actions"
      :key="idx"
      :elevation="0"
      style="margin: 0.5rem 0 0.5rem 0.5rem;"
      @click="dispatchAction(action)"
    >
      <IonIcon v-if="displayIcon(action)" class="action-icon" :name="action.icon"/>
      <span v-if="displayIcon(action) && displayLabel(action)" style="width: .5rem"/>
      <span v-if="displayLabel(action)">{{ labelText(action) }}</span>
    </v-btn>
  </v-row>
</template>

<script>
import IonIcon from 'vue-ionicon';

import EventEmitterMixin from '../public/event-emitter-mixin';

import Actions from './actions';

export default {
  name: 'VuetifyActions',
  components: { IonIcon },
  mixins: [Actions, EventEmitterMixin],
};
</script>

<style scoped>
  @import "actions.css";
</style>
