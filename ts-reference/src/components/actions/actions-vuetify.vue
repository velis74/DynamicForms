<template>
  <div v-if="actions != null && actions.length > 0" class="text-end">
    <v-btn
      v-for="(action,idx) in actions"
      :key="idx"
      :elevation="0"
      :class="idx === 0 ? '' : 'ms-3'"
      :size="isSmallSize(action) ? 'small' : 'default'"
      @click="(event) => dispatchAction(action, { event })"
      variant="tonal"
    >
      <IonIcon v-if="displayIcon(action)" class="action-icon" :name="action.icon"/>
      <span v-if="displayIcon(action) && displayLabel(action)" style="width: .5rem"/>
      <span v-if="displayLabel(action)">{{ labelText(action) }}</span>
    </v-btn>
  </div>
</template>

<script lang="ts">
import './actions.css';

import { defineComponent } from 'vue';

import IonIcon from 'vue-ionicon';

import ActionHandlerMixin from './action-handler.mixin';
import ActionsMixin from './actions.mixin';

export default defineComponent({
  name: 'VuetifyActions',
  components: { IonIcon },
  mixins: [ActionsMixin, ActionHandlerMixin],
});
</script>
