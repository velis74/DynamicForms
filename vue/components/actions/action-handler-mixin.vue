<script lang="ts">
import _ from 'lodash';
import { ComponentPublicInstance, defineComponent } from 'vue';

import Action from './action';
import FilteredActions from './filtered-actions';
import ActionHandler = Actions.ActionHandler;
import ActionHandlerExtraData = Actions.ActionHandlerExtraData;
import FormPayload = APIConsumer.FormPayload;

type HandlerWithPayload = { instance: { [key: string]: ActionHandler }, methodName: string, payload: FormPayload };

async function asyncSome(arr: HandlerWithPayload[], fun: (handler: HandlerWithPayload) => Promise<boolean>) {
  for (const e of arr) {
    // eslint-disable-next-line no-await-in-loop
    if (await fun(e)) return true;
  }
  return false;
}

function getHandlersWithPayload(
  action: Action,
  self: ComponentPublicInstance,
  actionName: string,
): HandlerWithPayload[] {
  // first, if action has a specific handler specified, let's just return that and be done with it
  if (action[`action${actionName}`]) {
    return [{ instance: action, methodName: `action${actionName}`, payload: action.payload }];
  }
  // WARNING: It is unlikely, but possible that a parent would handle the event, but not have a payload prop
  let parent = self;
  let payload = action.payload; // for some reason "this" got lost on this line, so I replaced it with self
  const res = [] as HandlerWithPayload[];
  while (parent != null) {
    // stop looking for action handler if the component has actions declared, but current action is not among them
    if ((parent.actions instanceof FilteredActions) && !parent.actions.hasAction(action)) break;

    if (parent.payload !== undefined) payload = parent.payload;
    if (parent[`action${actionName}`]) {
      res.unshift({ instance: parent, methodName: `action${actionName}`, payload });
    }
    parent = parent.$parent;
  }
  return res;
}

function emitEvent(self: ComponentPublicInstance, emitData: Object) {
  self.$emit(...emitData);
  let parent = self;
  while (parent != null) {
    if (['DfForm', 'DfTable', 'FormLayout'].indexOf(parent.$options.name as string) !== -1) {
      parent.$emit(...emitData);
      return;
    }
    parent = parent.$parent;
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
      const actionDFName = `${_.upperFirst(_.camelCase(_.toLower(action.name)))}`;

      let lastExecutedHandler;
      const handlers = [
        ...getHandlersWithPayload(action, this, actionDFName),
        ...getHandlersWithPayload(action, this, 'processActionsGeneric'),
      ];
      console.log('handlers', handlers);
      const actionHandled = await asyncSome(
        handlers,
        async (handler: HandlerWithPayload) => {
          lastExecutedHandler = handler;
          return (<ActionHandler>(handler.instance[handler.methodName] ??
            handler.instance.processActionsGeneric))(action, handler.payload, ed);
        },
      );
      if (!actionHandled && lastExecutedHandler) {
        // means action wasn't handled but some handlers were executed, return first handler
        lastExecutedHandler = handlers.shift();
      }
      emitEvent(this, ['action-executed', { action, handler: lastExecutedHandler?.payload, ed, actionHandled }]);
    },
  },
});
</script>
