import type { APIConsumer } from '../api_consumer/namespace';
import type FormPayload from '../form/definitions/form-payload';
import type DialogDefinition from '../modal/dialog-definition';
import type TableColumn from '../table/definitions/column';
import type RowTypes from '../table/definitions/row-types';

import type Action from './action';
import FilteredActions from './filtered-actions';

export namespace ActionsNS {

  export interface ActionHandlerExtraData {
    dialog?: DialogDefinition;
    field?: string;
    oldValue?: any;
    newValue?: any;
    event?: Event;
    column?: TableColumn;
    rowType?: RowTypes;
  }

  export type ActionHandler = (
    action: Action,
    payload: FormPayload | undefined,
    extraData: ActionHandlerExtraData
  ) => boolean;

  export interface BreakpointJSON {
    [key: string]: BreakpointsJSON | boolean | undefined;

    showLabel?: boolean;
    showIcon?: boolean;
    asButton?: boolean;
  }

  export interface BreakpointsJSON extends BreakpointJSON {
    [key: string]: BreakpointsJSON | boolean | undefined;

    xl?: BreakpointJSON;
    lg?: BreakpointJSON;
    md?: BreakpointJSON;
    sm?: BreakpointJSON;
    xs?: BreakpointJSON;
  }

  export interface ActionJSON {
    [key: `action${string}`]: ActionHandler;

    name?: string;
    label?: string;
    icon?: string;
    displayStyle?: BreakpointsJSON;
    position?: string;
    field_name?: string;
  }

  export interface ActionsJSON {
    [key: string]: ActionJSON;

    // @ts-ignore: don't know how else to get rid of TS2411 here and I really don't want a safe declaration for indexed
    payload: APIConsumer.FormPayloadJSON;
  }

  export interface ErrorsJSON {
    [key: string]: unknown; // TODO: we don't know yet what type this is
  }

  export type Handler = (...params: any[]) => Promise<boolean> | boolean;

  export interface IHandlers {
    [key: string]: Handler;
  }

  export interface IActionHandler {
    register: (actionName: string, handler: Handler) => this
    call: (action: Action | FilteredActions, context?: any) => Promise<boolean>
    recursiveCall: (
      action: Action | FilteredActions, actionPayload: any, context?: any, f2L?: boolean
    ) => Promise<boolean>
  }

  export interface ActionHandlerComposable {
    registerHandler: (actionName: string, handler: Handler) => void
    callHandler: (action: Action | FilteredActions, context?: any) => Promise<boolean>
    handler: IActionHandler
  }
}
