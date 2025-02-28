<template>
  <div v-if="actions != null && actions.length > 0" class="text-end">
    <v-btn
      v-for="(action, idx) in actions"
      :key="idx"
      variant="tonal"
      :elevation="0"
      :class="idx === 0 ? '' : 'ms-3'"
      :size="isSmallSize(action) ? 'small' : 'default'"
      :title="action.title"
      @click.stop="(event: MouseEvent) => callHandler(action, { event })"
    >
      <IonIcon v-if="displayIcon(action)" class="action-icon" :name="<string> action.icon"/>
      <span v-if="displayIcon(action) && displayLabel(action)" style="width: .5rem"/>
      <span v-if="displayLabel(action)">{{ labelText(action) }}</span>
    </v-btn>
  </div>
</template>

<script lang="ts">
import { defineComponent } from 'vue';
import IonIcon from 'vue-ionicon';
import { useDisplay } from 'vuetify';

import { useActionHandler } from './action-handler-composable';
import ActionHandlerMixin from './action-handler-mixin';
import ActionsMixin from './actions-mixin';

export default /* #__PURE__ */ defineComponent({
  name: 'VuetifyActions',
  components: { IonIcon },
  mixins: [ActionsMixin, ActionHandlerMixin],
  setup() {
    const { callHandler } = useActionHandler();
    const useDisplayInstance = useDisplay();
    // useDisplay is a prop that is needed in actions-mixin
    return {
      callHandler,
      useDisplay: useDisplayInstance as any,
      //   there must be "as any" because otherwise build returns error
      //   "Default export of the module has or is using private name 'DisplayPlatform'" due to
      //   private type "DisplayPlatform" that is used by component useDisplay from Vuetify, isn't correctly exported.
    };
  },
});
</script>

<style scoped>
.action-icon {
  width:  1.5em;
  height: 1.5em;
}
</style>
