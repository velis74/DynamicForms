import { camelCase, isBoolean, isObjectLike, isString, toLower, upperFirst } from 'lodash-es';

import FormPayload from '../form/definitions/form-payload';
import { gettext } from '../util/translations-mixin';

import type { ActionsNS } from './namespace';

type ActionHandlerExtraData = ActionsNS.ActionHandlerExtraData;
type ActionJSON = ActionsNS.ActionJSON;
type BreakpointJSON = ActionsNS.BreakpointJSON;
type BreakpointsJSON = ActionsNS.BreakpointsJSON;

let uniqueIdCounter = 0;
const ACTION_POSITIONS = [
  'HEADER', 'ROW_START', 'ROW_END', 'FIELD_START', 'FIELD_END', 'FORM_HEADER', 'FORM_FOOTER',
  'ROW_CLICK', 'ROW_RIGHT_CLICK', 'VALUE_CHANGED',
];

export function defaultActionHandler(
  action: Action,
  payload: FormPayload | undefined,
  extraData: ActionHandlerExtraData,
) {
  const dialog = extraData?.dialog;
  // console.log('Action execute:', action, payload, extraData);
  if (dialog && dialog.resolvePromise && dialog.close) {
    dialog.resolvePromise({ action, payload, extraData, dialog });
    dialog.close();
  }
  return true;
}

export function getActionName(actionName: string | undefined): `action${string}` {
  return `action${upperFirst(camelCase(toLower(actionName)))}`;
}

class Action implements ActionJSON {
  public name!: string;

  public uniqueId!: number;

  public position!: string;

  public fieldName!: string | null;

  public label?: string;

  public labelAvailable!: boolean;

  public icon?: string;

  public iconAvailable!: boolean;

  public displayStyle!: BreakpointsJSON;

  public payload!: FormPayload | undefined;

  public title?: string;

  [key: `action${string}`]: ActionsNS.ActionHandler;

  constructor(data: Action | ActionJSON, payload?: FormPayload) {
    const uniqueId = ++uniqueIdCounter;

    const name = data.name;
    const position = data.position;

    if (!isString(name) || !/^[a-zA-Z-_]+$/.test(name)) {
      console.warn(
        `Action name must be a valid string, matching [a-zA-Z-_]+. Got ${name}.` +
        ' Impossible to construct handler function name',
        data,
      );
    }

    // any non-string or empty string must resolve as null for label
    const label = !isString(data.label) || data.label.length === 0 ? null : data.label;
    // any non-string or empty string must resolve as null for icon
    const icon = !isString(data.icon) || data.icon.length === 0 ? null : data.icon;

    // displayStyle is an object of { breakpoint.{ showLabel, showIcon, asButton } } specs detailing how an action
    //  should be rendered at various breakpoints. A special case without a breakpoint is allowed specifying the common
    //  arrangement
    const displayStyleProps = ['asButton', 'showLabel', 'showIcon'];

    function displayStyleBreakpointClean(bp: BreakpointsJSON | undefined) {
      if (bp == null || !isObjectLike(bp)) return null;
      const cbp = displayStyleProps.reduce((res: BreakpointsJSON, p: string) => {
        if (isBoolean(bp[p])) res[p] = bp[p];
        return res;
      }, {});
      return Object.keys(cbp).length === 0 ? null : cbp;
    }

    function conditionalAddBreakpoint(ds: BreakpointsJSON, breakpoint: string) {
      if (data.displayStyle == null) return;
      const bpData = displayStyleBreakpointClean(data.displayStyle[breakpoint] as BreakpointJSON);
      if (bpData) ds[breakpoint] = bpData;
    }

    const displayStyle = displayStyleBreakpointClean(data.displayStyle) || {};
    // see also actions-mixin.ts about these breakpoints
    conditionalAddBreakpoint(displayStyle, 'xl');
    conditionalAddBreakpoint(displayStyle, 'lg');
    conditionalAddBreakpoint(displayStyle, 'md');
    conditionalAddBreakpoint(displayStyle, 'sm');
    conditionalAddBreakpoint(displayStyle, 'xs');

    if (ACTION_POSITIONS.indexOf(position as string) === -1) {
      console.warn(`Action position ${position} not known`, data);
    }

    const fieldNameTemp = data instanceof Action ? data.fieldName : data.field_name;
    // any non-string or empty string must resolve as null for fieldName
    const fieldName = !isString(fieldNameTemp) || fieldNameTemp.length === 0 ? null : fieldNameTemp;

    const title = !isString(data.title) || data.title.length === 0 ? null : data.title;

    const actionName = getActionName(data.name);
    this[actionName] = data[actionName];

    Object.defineProperties(this, {
      name: { get() { return name; }, enumerable: true },
      uniqueId: { get() { return uniqueId; }, enumerable: false },
      position: { get() { return position; }, enumerable: true },
      fieldName: { get() { return fieldName; }, enumerable: true },

      label: { get() { return label; }, enumerable: true },
      labelAvailable: { get() { return label != null; }, enumerable: true },
      icon: { get() { return icon; }, enumerable: true },
      iconAvailable: { get() { return icon != null; }, enumerable: true },
      displayStyle: { get() { return displayStyle; }, enumerable: true },
      title: { get() { return title; }, enumerable: true },

      payload: { get(): FormPayload | undefined { return payload; }, enumerable: true },
      // elementType & bindAttrs, entire action.action concept:
      //   action.py && actionsHandler.decorateActions, added by brontes, modified by velis
      //   not sure this is necessary: I have only found one instance of action declaration in python and
      //   it's just so a dialog can be shown. Doubt it even worked at any time. Also that same thing is now
      //   solved via parent components declaring action handler methods
    });
  }

  static closeAction(data: ActionJSON = {}) {
    return new Action({
      name: 'close',
      label: gettext('Close'),
      icon: 'close-outline',
      displayStyle: { asButton: true, showLabel: true, showIcon: true },
      position: 'FORM_FOOTER',
      ...data, // any properties in data should overwrite properties in the constant
    });
  }

  static yesAction(data: ActionJSON = {}) {
    return new Action({
      name: 'yes',
      label: gettext('Yes'),
      icon: 'thumbs-up-outline',
      displayStyle: { asButton: true, showLabel: true, showIcon: true },
      position: 'FORM_FOOTER',
      ...data, // any properties in data should overwrite properties in the constant
    });
  }

  static noAction(data: ActionJSON = {}) {
    return new Action({
      name: 'no',
      label: gettext('No'),
      icon: 'thumbs-down-outline',
      displayStyle: { asButton: true, showLabel: true, showIcon: true },
      position: 'FORM_FOOTER',
      ...data, // any properties in data should overwrite properties in the constant
    });
  }
}

export default Action;
