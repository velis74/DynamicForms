// eslint-disable-next-line max-classes-per-file
import { inject, provide } from 'vue';

export type Handler = (...params: any[]) => Promise<boolean> | boolean;

export interface IActionHandler {
  [key: string]: Handler;
}

export interface IActionMethods {
  register: (actionName: string, handler: Handler) => this
  call: (actionName: string, ...params: any[]) => Promise<boolean>
}

export interface ActionHandlerComposable {
  registerHandler: (actionName: string, handler: Handler) => void
  callHandler: (actionName: string, ...params: any[]) => Promise<boolean>
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

  const callHandler = async (actionName: string, ...params: any[]): Promise<boolean> => {
    console.log('calling', actionName, params);
    return actionHandler[actionName](firstToLast, params);
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
