import { defineComponent } from 'vue';

import DisplayBreakpointsMixin from '@/components/util/display-breakpoints.mixin';

import FilteredActions from '@/components/actions/filtered-actions';
import type Action from '@/components/actions/action';

export default defineComponent({
  props: { actions: { type: FilteredActions, default: null } },
  mixins: [DisplayBreakpointsMixin],
  computed: {
    displayStyle() {
      const res: any = {};
      for (const action of this.actions) { // eslint-disable-line no-restricted-syntax
        let actionRes: any = {};
        if (action.displayStyle) {
          this.checkStyle('asButton', actionRes, action.displayStyle);
          this.checkStyle('showIcon', actionRes, action.displayStyle);
          this.checkStyle('showLabel', actionRes, action.displayStyle);
        }
        actionRes = {
          asButton: actionRes.asButton !== undefined ? actionRes.asButton : false,
          showIcon: actionRes.showIcon !== undefined ? actionRes.showIcon : true,
          showLabel: actionRes.showLabel !== undefined ? actionRes.showLabel : true,
        };
        res[action.name] = actionRes;
      }
      return res;
    },
  },
  methods: {
    checkStyle(attribute: string, actionRes: any, displayStyle: any) {
      let style;
      console.log(this.screen_breakpoints);
      // see also action.js about these breakpoints
      if (displayStyle.xl && displayStyle.xl[attribute] !== undefined && this.screen_breakpoints.xlOnly) {
        style = displayStyle.xl[attribute];
      } else if (displayStyle.lg && displayStyle.lg[attribute] !== undefined && this.screen_breakpoints.lgAndUp) {
        style = displayStyle.lg[attribute];
      } else if (displayStyle.md && displayStyle.md[attribute] !== undefined && this.screen_breakpoints.mdAndUp) {
        style = displayStyle.md[attribute];
      } else if (displayStyle.sm && displayStyle.sm[attribute] !== undefined && this.screen_breakpoints.smAndUp) {
        style = displayStyle.sm[attribute];
      } else if (displayStyle.xs && displayStyle.xs[attribute] !== undefined) {
        style = displayStyle.xs[attribute];
      } else if (displayStyle[attribute] !== undefined) {
        style = displayStyle[attribute];
      }
      actionRes[attribute] = style;
    },
    asText(action: Action): boolean {
      return !this.displayStyle[action.name].asButton;
    },
    asIcon(action: Action): boolean {
      return !this.showLabel(action);
    },
    buttonVariant(action: Action): string {
      return this.displayStyle[action.name].asButton ? 'info' : 'link';
    },
    displayIcon(action: Action): boolean {
      return this.displayStyle[action.name].showIcon && action.iconAvailable;
    },
    displayLabel(action: Action): boolean {
      if (this.displayStyle[action.name].showLabel && action.labelAvailable) return true;
      return !(this.displayStyle[action.name].showIcon && action.iconAvailable);
    },
    labelText(action: Action): string {
      if (action.labelAvailable) return action.label;
      return action.name;
    },
    isSmallSize(action: Action): boolean {
      return action.position !== 'HEADER' && action.position !== 'FORM_FOOTER';
    },
  },
});
