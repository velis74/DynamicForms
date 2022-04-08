<template>
  <div v-if="actions != null && actions.length > 0" class="dynamicforms-actioncontrol">
    <b-button
      v-for="action in actions"
      :key="action.name + action.icon"
      :variant="buttonVariant(action)"
      size="sm"
    >
      <IonIcon :class="iconClass(action)" class="action-icon" :name="action.icon"/>
      <span :class="marginClass(action)" style="width: .5rem"/>
      <span :class="labelClass(action)">{{ action.label }}</span>
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
    buttonVariant(action) {
      return this.displayStyle[action.name].asButton ? 'info' : 'link';
    },
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
    getVisibilityClass(visible) {
      return visible ? 'd-inline-block' : 'd-none';
    },
  },
};
</script>

<style scoped>
  @import "actions.css";
</style>
