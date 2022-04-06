<template>
  <div v-if="actionList != null && actionList.length > 0">
    <v-btn
      v-for="action in actionList"
      :key="action.name + action.icon"
      :text="!getDisplayStyle(action).asButton"
      :icon="!getDisplayStyle(action).showLabel"
      :x-small="true"
      :elevation="0"
    >
      <IonIcon v-if="getDisplayStyle(action).showIcon" class="action-icon" :name="action.icon"/>
      <span v-if="getDisplayStyle(action).showIcon && getDisplayStyle(action).showLabel" style="width: .5rem"/>
      <span v-if="getDisplayStyle(action).showLabel">{{ action.label }}</span>
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
  methods: {
    getDisplayStyle(action) {
      let res = this.displayStyle[action];
      if (res == null) {
        res = {};
      }
      this.displayStyle[action] = res;
      res = res[this.$vuetify.breakpoint.name];

      if (res == null) {
        res = {};
        if (action.displayStyle) {
          if (action.displayStyle.xl && this.$vuetify.breakpoint.xl) {
            res = action.displayStyle.xl;
          } else if (action.displayStyle.lg && this.$vuetify.breakpoint.lgAndUp) {
            res = action.displayStyle.lg;
          } else if (action.displayStyle.md && this.$vuetify.breakpoint.mdAndUp) {
            res = action.displayStyle.md;
          } else if (action.displayStyle.sm && this.$vuetify.breakpoint.smAndUp) {
            res = action.displayStyle.sm;
          } else if (action.displayStyle.xs) {
            res = action.displayStyle.xs;
          } else {
            res = action.displayStyle;
          }
        }
        res = {
          asButton: this.getBoolValueOrDef(res.asButton, false),
          showIcon: this.getBoolValueOrDef(res.showIcon, true),
          showLabel: this.getBoolValueOrDef(res.showLabel, true),
        };
        this.displayStyle[action][this.$vuetify.breakpoint.name] = res;
      }
      return res;
    },
  },
};
</script>

<style scoped>

.action-icon {
  width:  0.875rem;
  height: 0.875rem
}

</style>
