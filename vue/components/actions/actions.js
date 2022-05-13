import DisplayBreakpoints from '../util/display_breakpoints';

export default {
  props: { actions: { type: Array, default: null } },
  mixins: [DisplayBreakpoints],
  computed: {
    displayStyle() {
      const res = {};
      const actionsLen = this.actions.length;
      for (let actInd = 0; actInd < actionsLen; actInd++) {
        const action = this.actions[actInd];
        let actionRes = {};
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
    checkStyle(attribute, actionRes, displayStyle) {
      let style;
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
    asText(action) {
      return !this.displayStyle[action.name].asButton;
    },
    asIcon(action) {
      return !this.showLabel(action);
    },
    buttonVariant(action) {
      return this.displayStyle[action.name].asButton ? 'info' : 'link';
    },
    getVisibilityClass(visible) {
      return visible ? 'd-inline-block' : 'd-none';
    },
  },
};
