<template>
  <div v-if="actions != null && actions.length > 0" class="text-end">
    <v-btn
      v-for="(action,idx) in actions"
      :key="idx"
      :elevation="0"
      :class="idx === 0 ? '' : 'ms-3'"
      :small="isSmallSize(action)"
      @click="(event) => dispatchAction(action, { event })"
    >
      <IonIcon v-if="displayIcon(action)" class="action-icon" :name="action.icon"/>
      <span v-if="displayIcon(action) && displayLabel(action)" style="width: .5rem"/>
      <span v-if="displayLabel(action)">{{ labelText(action) }}</span>
    </v-btn>
  </div>
</template>

<script>
import IonIcon from 'vue-ionicon';

import ActionHandlerMixin from './action-handler-mixin';
import ActionsMixin from './actions-mixin';

export default {
  name: 'VuetifyActions',
  components: { IonIcon },
  mixins: [ActionsMixin, ActionHandlerMixin],
};
</script>

<style scoped>
  @import "actions.css";
</style>
