// eslint-disable-next-line max-classes-per-file
import { inject, provide } from 'vue';

import Action from './action';
import FilteredActions from './filtered-actions';

export type Handler = (...params: any[]) => Promise<boolean> | boolean;

export interface IHandlers {
  [key: string]: Handler;
}

export interface IActionHandler {
  register: (actionName: string, handler: Handler) => this
  call: (action: Action | FilteredActions, context?: any) => Promise<boolean>
  recursiveCall: (action: Action | FilteredActions, actionPayload: any, context?: any) => Promise<boolean>
}

export interface ActionHandlerComposable {
  registerHandler: (actionName: string, handler: Handler) => void
  callHandler: (action: Action | FilteredActions, payload?: any, context?: any) => Promise<boolean>
  handler: IActionHandler
}

class Handlers implements IHandlers {
  [key: string]: Handler;
}

export function useActionHandler(firstToLast: boolean = true): ActionHandlerComposable {
  const parentHandler = inject<IActionHandler | undefined>('actionHandler', undefined);
  const payload = inject<any>('payload', {});

  class ActionHandlers implements IActionHandler {
    private handlers: Handlers = new Handlers();

    register = (actionName: string, handler: Handler) => {
      this.handlers[actionName] = handler;
      return this;
    };

    call = async (actions: Action | FilteredActions, context?: any): Promise<boolean> => (
      this.recursiveCall(actions, payload.value, context)
    );

    recursiveCall = async (actions: Action | FilteredActions, actionPayload?: any, context?: any): Promise<boolean> => {
      if (firstToLast) {
        return (
          await this.executeHandler(actions, actionPayload, context) ||
          (await parentHandler?.recursiveCall(actions, actionPayload, context) ?? false)
        );
      }
      return (
        (await parentHandler?.recursiveCall(actions, actionPayload, context) ?? false) ||
        await this.executeHandler(actions, actionPayload, context)
      );
    };

    private executeHandler = async (
      actions: Action | FilteredActions,
      actionPayload: any,
      context?: any,
    ): Promise<boolean> => {
      if (actions instanceof FilteredActions) {
        for (const action of actions) {
          const ed = { ...action.payload?.['$extra-data'], ...context };
          // eslint-disable-next-line no-await-in-loop
          if (await this.handlers[action.name]?.(action, actionPayload, ed)) return true;
        }
        return false;
      }
      const ed = { ...actions.payload?.['$extra-data'], ...context };
      return this.handlers[actions.name]?.(actions, actionPayload, ed) ?? false;
    };
  }

  const handler = new ActionHandlers();

  const callHandler = handler.call;
  const registerHandler = handler.register;

  provide('actionHandler', handler);

  return { registerHandler, callHandler, handler };
}
