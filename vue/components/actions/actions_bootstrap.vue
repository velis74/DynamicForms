<template>
  <div v-if="actions != null && actions.length > 0" class="dynamicforms-actioncontrol">
    <b-button
      v-for="action in actions"
      :key="action.name + action.icon"
      :variant="buttonVariant(action)"
      size="sm"
    >
      <IonIcon :class="displayIcon(action)" class="action-icon d-inline-block" :name="action.icon"/>
      <span :class="marginClass(action)" style="width: .5rem"/>
      <span :class="displayLabel(action)">{{ labelText(action) }}</span>
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
    iconClass(action) {
      return this.getVisibilityClass(this.displayStyle[action.name].showIcon);
    },
    labelClass(action) {
      return this.getVisibilityClass(this.displayStyle[action.name].showLabel);
    },
    marginClass(action) {
      return this.getVisibilityClass(this.displayStyle[action.name].showIcon &&
        this.displayStyle[action.name].showLabel);
    },
  },
};
</script>

<style scoped>
  @import "actions.css";
</style>
