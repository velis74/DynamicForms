import _ from 'lodash';

let uniqueIdCounter = 0;
const ACTION_POSITIONS = [
  'HEADER', 'ROW_START', 'ROW_END', 'FIELD_START', 'FIELD_END', 'FORM_HEADER', 'FORM_FOOTER',
];

class Action {
  constructor(data) {
    const uniqueId = ++uniqueIdCounter;

    if (!_.isString(data.name) || !/^[a-zA-Z-_]+$/.test(data.name)) {
      console.warn(
        `Action name must be a valid string, matching [a-zA-Z-_]+. Got ${data.name}.` +
        ' Impossible to construct handler function name',
        data,
      );
    }

    // any non-string or empty string must resolve as null for label
    const label = !_.isString(data.label) || data.label.length === 0 ? null : data.label;
    // any non-string or empty string must resolve as null for icon
    const icon = !_.isString(data.icon) || data.icon.length === 0 ? null : data.icon;

    // displayStyle is an object of { breakpoint.{ showLabel, showIcon, asButton } } specs detailing how an action
    //  should be rendered at various breakpoints. A special case without a breakpoint is allowed specifying the common
    //  arrangement
    const displayStyleProps = ['asButton', 'showLabel', 'showIcon'];

    function displayStyleBreakpointClean(bp) {
      if (!_.isObjectLike(bp)) return null;
      const cbp = displayStyleProps.reduce((res, p) => {
        if (_.isBoolean(bp[p])) res[p] = bp[p];
        return res;
      }, {});
      return Object.keys(cbp).length === 0 ? null : cbp;
    }

    function conditionalAddBreakpoint(ds, breakpoint) {
      if (data.displayStyle == null) return;
      const bpData = displayStyleBreakpointClean(data.displayStyle[breakpoint]);
      if (bpData) ds[breakpoint] = bpData;
    }

    const displayStyle = displayStyleBreakpointClean(data.displayStyle) || {};
    // see also actions-mixin.js about these breakpoints
    conditionalAddBreakpoint(displayStyle, 'xl');
    conditionalAddBreakpoint(displayStyle, 'lg');
    conditionalAddBreakpoint(displayStyle, 'md');
    conditionalAddBreakpoint(displayStyle, 'sm');
    conditionalAddBreakpoint(displayStyle, 'xs');

    if (ACTION_POSITIONS.indexOf(data.position) === -1) {
      console.warn(`Action position ${data.position} not known`, data);
    }
    // any non-string or empty string must resolve as null for fieldName
    const fieldName = !_.isString(data.field_name) || data.field_name.length === 0 ? null : data.field_name;

    Object.defineProperties(this, {
      name: { get() { return data.name; }, enumerable: true },
      uniqueId: { get() { return uniqueId; }, enumerable: false },
      position: { get() { return data.position; }, enumerable: true },
      fieldName: { get() { return fieldName; }, enumerable: true },

      label: { get() { return label; }, enumerable: true },
      labelAvailable: { get() { return label != null; }, enumerable: true },
      icon: { get() { return icon; }, enumerable: true },
      iconAvailable: { get() { return icon != null; }, enumerable: true },
      displayStyle: { get() { return displayStyle; }, enumerable: true },
      // elementType & bindAttrs, entire action.action concept:
      //   action.py && actionsHandler.decorateActions, added by brontes, modified by velis
      //   not sure this is necessary: I have only found one instance of action declaration in python and
      //   it's just so a dialog can be shown. Doubt it even worked at any time. Also that same thing is now
      //   solved via parent components declaring action handler methods
    });
  }
}

export default Action;
