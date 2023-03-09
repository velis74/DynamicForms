import { ComponentPublicInstance, defineComponent } from 'vue';

import { APIConsumer } from '../api_consumer/namespace';

import Action, { getActionName } from './action';
import ActionsMixin from './actions-mixin';
import FilteredActions from './filtered-actions';

import ActionHandler = Actions.ActionHandler;
import ActionHandlerExtraData = Actions.ActionHandlerExtraData;
import FormPayload = APIConsumer.FormPayload;

type ObjectWithActionHandler = { [key: `action${string}`]: ActionHandler };
type HandlerWithPayload = { instance: ObjectWithActionHandler, methodName: string, payload: FormPayload };
type ComponentWithActionsAndHandler =
  ComponentPublicInstance & (InstanceType<typeof ActionsMixin> & ObjectWithActionHandler & { payload: any });

async function asyncSome(arr: HandlerWithPayload[], fun: (handler: HandlerWithPayload) => Promise<boolean>) {
  for (const e of arr) {
    // eslint-disable-next-line no-await-in-loop
    if (await fun(e)) return true;
  }
  return false;
}

function getHandlersWithPayload(
  action: Action,
  self: ComponentWithActionsAndHandler,
  actionName: `action${string}`,
): HandlerWithPayload[] {
  // first, if action has a specific handler specified, let's just return that and be done with it
  if (action[actionName]) {
    return [{ instance: action, methodName: actionName, payload: action.payload }];
  }
  // WARNING: It is unlikely, but possible that a parent would handle the event, but not have a payload prop
  let parent = self;
  let payload = action.payload; // for some reason "this" got lost on this line, so I replaced it with self
  const res = [] as HandlerWithPayload[];
  while (parent != null) {
    // stop looking for action handler if the component has actions declared, but current action is not among them
    if ((parent.actions instanceof FilteredActions) && !parent.actions.hasAction(action)) break;

    if (parent.payload !== undefined) payload = parent.payload;
    if (parent[actionName]) {
      res.unshift({ instance: parent, methodName: actionName, payload });
    }
    parent = parent.$parent as ComponentWithActionsAndHandler;
  }
  return res;
}

function emitEvent(
  self: ComponentPublicInstance,
  emitData: [string, { action: any, payload: any, ed: any, actionHandled: boolean }],
) {
  self.$emit(...emitData);
  let parent = self;
  while (parent != null) {
    if (['DfForm', 'DfTable', 'DfFormLayout'].indexOf(parent.$options.name as string) !== -1) {
      parent.$emit(...emitData);
      return;
    }
    parent = parent.$parent as ComponentPublicInstance;
  }
}

export default /* #__PURE__ */ defineComponent({
  name: 'ActionHandlerMixin',
  methods: {
    /**
     * Action is handled by a specific function on a component. First parent component which has this function
     * defined executes this function with arguments actionData, payload. Payload is a computed variable, for payload
     * value, value of first parent component's payload computed value is taken if payload computed var is defined.
     * If this function returns false then current component tries to execute functionName(payload)
     *
     * Function name which executes action data is "calculated from actionData attributes."
     *
     * @param actions: Action
     * @param extraData: object - e.g. { fieldName: 'field' }
     */
    async dispatchAction(actions: Action | FilteredActions, extraData: ActionHandlerExtraData) {
      if (actions instanceof FilteredActions) {
        // Takes care of situations where we just call dispatchAction with filtered actions list. We don't care whether
        // there is one action or many: we just execute them all
        for (const act of actions) {
          this.dispatchAction(act, extraData);
        }
        return;
      }

      const action = actions;
      const ed = { ...action.payload?.['$extra-data'], ...extraData };
      const actionDFName = getActionName(action.name);

      let lastExecutedHandler;
      const handlers = [
        ...getHandlersWithPayload(action, <ComponentWithActionsAndHandler> <unknown> this, actionDFName),
        ...getHandlersWithPayload(
          action,
          <ComponentWithActionsAndHandler> <unknown> this,
          'actionDefaultProcessor',
        ),
      ];
      // console.log('handlers', handlers, 'action', action);
      const actionHandled = await asyncSome(
        handlers,
        async (handler: HandlerWithPayload) => {
          lastExecutedHandler = handler;
          return (<ActionHandler> (handler.instance[handler.methodName as `action${string}`] ??
            handler.instance.actionDefaultProcessor))(action, handler.payload, ed);
        },
      );
      if (!actionHandled && lastExecutedHandler) {
        // means action wasn't handled but some handlers were executed, return first handler
        lastExecutedHandler = handlers.shift();
      }
      emitEvent(this, ['action-executed', { action, payload: lastExecutedHandler?.payload, ed, actionHandled }]);
    },
  },
});
