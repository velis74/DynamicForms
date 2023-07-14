// eslint-disable-next-line max-classes-per-file
import { inject, provide } from 'vue';

import Action from './action';
import FilteredActions from './filtered-actions';

export type Handler = (...params: any[]) => Promise<boolean> | boolean;

export interface IActionHandler {
  [key: string]: Handler;
}

export interface IActionMethods {
  register: (actionName: string, handler: Handler) => this
  call: (action: Action | FilteredActions, context?: any) => Promise<boolean>
}

export interface ActionHandlerComposable {
  registerHandler: (actionName: string, handler: Handler) => void
  callHandler: (action: Action | FilteredActions, payload?: any, context?: any) => Promise<boolean>
  handler: IActionMethods
}

class ActionHandler implements IActionHandler {
  [key: string]: Handler;
}

const RecurseHandler = (oldActionHandler: ActionHandler) => new Proxy<ActionHandler>(new ActionHandler(), {
  get(target: ActionHandler, key: string) {
    return async (firstToLast: boolean, params: any[]) => {
      if (firstToLast) {
        return await target?.[key]?.(...params) || !!oldActionHandler?.[key]?.(firstToLast, params);
      }
      return !!oldActionHandler?.[key]?.(firstToLast, params) || await target?.[key]?.(...params);
    };
  },
});

export function useActionHandler(firstToLast: boolean = true): ActionHandlerComposable {
  const actionHandler = RecurseHandler(inject<ActionHandler>('actionHandler', new ActionHandler()));

  provide('actionHandler', actionHandler);

  const registerHandler = (actionName: string, handler: Handler): void => {
    actionHandler[actionName] = handler;
  };

  const callHandler = async (actions: Action | FilteredActions, payload?: any, context?: any): Promise<boolean> => {
    console.log('YES');
    if (actions instanceof FilteredActions) {
      for (const action of actions) {
        console.log(action.name);
        const ed = { ...action.payload?.['$extra-data'], ...context };
        if (actionHandler[action.name](firstToLast, [actions, payload, ed])) return true;
      }
      return false;
    }
    console.log(actions.name);
    const ed = { ...actions.payload?.['$extra-data'], ...context };
    return actionHandler[actions.name](firstToLast, [actions, payload, ed]);
  };

  class ActionMethods implements IActionMethods {
    register = (actionName: string, handler: Handler) => {
      registerHandler(actionName, handler);
      return this;
    };

    call = callHandler;
  }

  return { registerHandler, callHandler, handler: new ActionMethods() };
}
