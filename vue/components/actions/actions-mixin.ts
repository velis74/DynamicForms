import { defineComponent } from 'vue';

import DisplayBreakpoints from '../util/breakpoints-display';

import Action from './action';
import FilteredActions from './filtered-actions';
import BreakpointJSON = Actions.BreakpointJSON;
import BreakpointsJSON = Actions.BreakpointsJSON;

// noinspection PointlessBooleanExpressionJS
export default /* #__PURE__ */ defineComponent({
  mixins: [DisplayBreakpoints],
  props: { actions: { type: FilteredActions, default: null } },
  computed: {
    displayStyle() {
      const res: BreakpointJSON = {};
      for (const action of this.actions) { // eslint-disable-line no-restricted-syntax
        let actionRes: BreakpointJSON = {};
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
    checkStyle(attribute: string, actionRes: BreakpointJSON, displayStyle: BreakpointsJSON) {
      let style;
      // see also action.ts about these breakpoints
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
    asText(action: Action) {
      return !(this.displayStyle[action.name] as BreakpointJSON).asButton;
    },
    buttonVariant(action: Action) {
      return (this.displayStyle[action.name] as BreakpointJSON).asButton ? 'info' : 'link';
    },
    displayIcon(action: Action): boolean {
      // noinspection PointlessBooleanExpressionJS
      return !!((this.displayStyle[action.name] as BreakpointJSON).showIcon && action.iconAvailable);
    },
    displayLabel(action: Action): boolean {
      if ((this.displayStyle[action.name] as BreakpointJSON).showLabel && action.labelAvailable) return true;
      return !((this.displayStyle[action.name] as BreakpointJSON).showIcon && action.iconAvailable);
    },
    labelText(action: Action): string {
      if (action.labelAvailable) return action.label as string;
      return action.name;
    },
    isSmallSize(action: Action): boolean {
      return action.position !== 'HEADER' && action.position !== 'FORM_FOOTER';
    },
  },
});
