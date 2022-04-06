<template>
  <div v-if="actionList != null && actionList.length > 0" class="dynamicforms-actioncontrol">
    <button
      v-for="action in actionList"
      :key="action.name + action.icon"
      class="btn btn-info btn-sm"
    >
      <IonIcon :class="getDisplayStyle(action).showIcon" class="action-icon" :name="action.icon"/>
      <span :class="getDisplayStyle(action).showMargin" style="width: .5rem"/>
      <span :class="getDisplayStyle(action).showLabel">{{ action.label }}</span>
    </button>
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
    getDisplayStyle(action) {
      // TODO: Bootstrap button doesn't have button type like "text" in vuetify...
      //  so we currently don't support it in bootstrap.
      let res = this.displayStyle[action];
      const iconClasses = {};
      const labelClasses = {};

      const iconClassesList = [];
      const labelClassesList = [];
      const marginClassesList = [];

      if (res == null) {
        res = { iconClass: '', labelClass: '' };
        if (action.displayStyle) {
          // We find display values for all sizes... if they are set. And than for specific sizes xs, sm, ..., xl
          // Than we look from smallest to largest size, and set classes.
          // If class is not defined for size we take one from previous size.
          this.checkStyle(action.displayStyle, 'xs', iconClasses, labelClasses);
          this.checkStyle(action.displayStyle.xs, 'xs', iconClasses, labelClasses);
          this.checkStyle(action.displayStyle.sm, 'sm', iconClasses, labelClasses);
          this.checkStyle(action.displayStyle.md, 'md', iconClasses, labelClasses);
          this.checkStyle(action.displayStyle.lg, 'lg', iconClasses, labelClasses);
          this.checkStyle(action.displayStyle.xl, 'xl', iconClasses, labelClasses);
        }
        this.checkStyle({ showLabel: true, showIcon: true }, 'def', iconClasses, labelClasses);

        let iconClass = iconClasses.def;
        let labelClass = labelClasses.def;
        const breakpoints = ['xs', 'sm', 'md', 'lg', 'xl'];
        const breakpointsLength = breakpoints.length;
        for (let i = 0; i < breakpointsLength; i++) {
          const breakpoint = breakpoints[i];

          if (breakpoint in iconClasses) {
            iconClass = iconClasses[breakpoint];
          }
          if (breakpoint in labelClasses) {
            labelClass = labelClasses[breakpoint];
          }
          let iconClassInsert = iconClass;
          let labelClassInsert = labelClass;
          if (breakpoint !== 'xs') {
            iconClassInsert = iconClassInsert.replace('d-', `d-${breakpoint}-`);
            labelClassInsert = labelClassInsert.replace('d-', `d-${breakpoint}-`);
          }
          iconClassesList.push(iconClassInsert);
          labelClassesList.push(labelClassInsert);
          let marginClassInsert = iconClassInsert;
          if (labelClassInsert.includes('-none')) {
            marginClassInsert = labelClassInsert;
          }
          marginClassesList.push(marginClassInsert);
        }

        res = {
          showIcon: iconClassesList.join(' '),
          showLabel: labelClassesList.join(' '),
          showMargin: marginClassesList.join(' '),
        };
        this.displayStyle[action] = res;
      }
      return res;
    },
    checkStyle(style, breakpoint, iconClasses, labelClasses) {
      if (style) {
        const classShow = 'd-inline-block';
        const classHide = 'd-none';

        if ('showIcon' in style) {
          iconClasses[breakpoint] = style.showIcon ? classShow : classHide;
        }
        if ('showLabel' in style) {
          labelClasses[breakpoint] = style.showLabel ? classShow : classHide;
        }
      }
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
