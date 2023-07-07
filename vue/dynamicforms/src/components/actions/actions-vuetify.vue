<template>
  <div v-if="actions != null && actions.length > 0" class="text-end">
    <v-btn
      v-for="(action, idx) in actions"
      :key="idx"
      variant="tonal"
      :elevation="0"
      :class="idx === 0 ? '' : 'ms-3'"
      :size="isSmallSize(action) ? 'small' : 'default'"
      @click.stop="(event: MouseEvent) => callHandler(action.name, action, { event })"
    >
      <IonIcon v-if="displayIcon(action)" class="action-icon" :name="<string> action.icon"/>
      <span v-if="displayIcon(action) && displayLabel(action)" style="width: .5rem"/>
      <span v-if="displayLabel(action)">{{ labelText(action) }}</span>
    </v-btn>
  </div>
</template>

<script lang="ts">
import { defineComponent } from 'vue';
import './actions.css';
import IonIcon from 'vue-ionicon';

import { useActionHandler } from './action-handler-composable';
import ActionHandlerMixin from './action-handler-mixin';
import ActionsMixin from './actions-mixin';

export default /* #__PURE__ */ defineComponent({
  name: 'VuetifyActions',
  components: { IonIcon },
  mixins: [ActionsMixin, ActionHandlerMixin],
  setup() {
    const { callHandler } = useActionHandler();
    return { callHandler };
  },
});
</script>
