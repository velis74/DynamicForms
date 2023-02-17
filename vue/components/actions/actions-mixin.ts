import { defineComponent } from 'vue';

import { useDisplay } from '../util/breakpoints';
import BreakpointsInterface from '../util/breakpoints-interface';

import Action from './action';
import FilteredActions from './filtered-actions';

import BreakpointJSON = Actions.BreakpointJSON;
import BreakpointsJSON = Actions.BreakpointsJSON;

// noinspection PointlessBooleanExpressionJS
export default /* #__PURE__ */ defineComponent({
  props: { actions: { type: FilteredActions, required: true } },
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
          asButton: actionRes.asButton != null ? actionRes.asButton : false,
          showIcon: actionRes.showIcon != null ? actionRes.showIcon : true,
          showLabel: actionRes.showLabel != null ? actionRes.showLabel : true,
        };
        res[action.name] = actionRes;
      }
      return res;
    },
  },
  methods: {
    checkStyle(attribute: string, actionRes: BreakpointJSON, displayStyle: BreakpointsJSON) {
      let style: any = null;
      const dp = useDisplay() as BreakpointsInterface;
      const getStyle = (s: BreakpointJSON | undefined) => (s && s[attribute] !== undefined ? s[attribute] : style);
      // see also action.ts about these breakpoints
      if (dp.xlOnly) style = getStyle(displayStyle.xl);
      if (style == null && dp.lgAndUp) style = getStyle(displayStyle.lg);
      if (style == null && dp.mdAndUp) style = getStyle(displayStyle.md);
      if (style == null && dp.smAndUp) style = getStyle(displayStyle.sm);
      if (style == null) {
        style = getStyle(displayStyle); // first we try to get base style
        style = getStyle(displayStyle.xs); // then xs, if it exists. xs will overwrite the base declaration
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
      return !this.displayIcon(action);
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
