<template>
  <div v-if="actions != null && actions.length > 0" class="dynamicforms-actioncontrol text-right">
    <b-button
      v-for="(action, idx) in actions"
      :key="idx"
      :variant="buttonVariant(action)"
      :class="idx === 0 ? '' : 'ml-3'"
      :size="isSmallSize(action) ? 'xs' : 'sm'"
    >
      <IonIcon :class="`action-icon ${iconClass(action)}`" :name="action.icon"/>
      <span :class="marginClass(action)" style="width: .5rem"/>
      <span :class="labelClass(action)">{{ labelText(action) }}</span>
    </b-button>
  </div>
</template>

<script>
import IonIcon from 'vue-ionicon';

import ActionsMixin from './actions-mixin';

export default {
  name: 'BootstrapActions',
  components: { IonIcon },
  mixins: [ActionsMixin],
  methods: {
    getVisibilityClass(visible) {
      return visible ? 'd-inline-block' : 'd-none';
    },
    iconClass(action) {
      return this.getVisibilityClass(this.displayIcon(action));
    },
    labelClass(action) {
      return this.getVisibilityClass(this.displayLabel(action));
    },
    marginClass(action) {
      return this.getVisibilityClass(this.displayIcon(action) && this.displayLabel(action));
    },
  },
};
</script>

<style scoped>
  @import "actions.css";
</style>
