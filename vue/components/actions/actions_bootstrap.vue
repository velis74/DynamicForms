<template>
  <div v-if="actions != null && actions.length > 0" class="dynamicforms-actioncontrol">
    <b-button
      v-for="action in actions"
      :key="action.name + action.icon"
      :variant="buttonVariant(action)"
      size="sm"
    >
      <IonIcon :class="`action-icon ${iconClass(action)}`" :name="action.icon"/>
      <span :class="marginClass(action)" style="width: .5rem"/>
      <span :class="labelClass(action)">{{ labelText(action) }}</span>
    </b-button>
  </div>
</template>

<script>
import IonIcon from 'vue-ionicon';

import Actions from './actions';

export default {
  name: 'BootstrapActions',
  components: { IonIcon },
  mixins: [Actions],
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
