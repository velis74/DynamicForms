import type { APIConsumer } from '../api_consumer/namespace';
import type FormPayload from '../form/definitions/form-payload';
import type DialogDefinition from '../modal/dialog-definition';

import type Action from './action';

export namespace Actions {

  export interface ActionHandlerExtraData {
    dialog?: DialogDefinition;
  }

  export type ActionHandler = (
    action: Action,
    payload: FormPayload,
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

    // @ts-ignore
    payload: APIConsumer.FormPayloadJSON;
  }

  export interface ErrorsJSON {
    [key: string]: unknown; // TODO: we don't know yet what type this is
  }
}
