<script>
import _ from 'lodash';

import FilteredActions from './filtered-actions';

export default {
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
     * @param action: Action
     * @param extraData: object - e.g. { fieldName: 'field' }
     */
    async dispatchAction(action, extraData) {
      if (action instanceof FilteredActions) {
        // Takes care of situations where we just call dispatchAction with filtered actions list. We don't care whether
        // there is one action or many: we just execute them all
        for (const act of action) {
          this.dispatchAction(act, extraData);
        }
      }
      const actionDFName = `action${_.upperFirst(_.camelCase(_.toLower(action.name)))}`;

      function getHandlersWithPayload(self, actionName) {
        // first, if action has a specific handler specified, let's just return that and be done with it
        if (action.handlerWithPayload) return [action.handlerWithPayload];
        // WARNING: It is unlikely, but possible that a parent would handle the event, but not have a payload prop
        let parent = self;
        let payload = action.payload; // for some reason "this" got lost on this line, so I replaced it with self
        const res = [];
        while (parent != null) {
          // stop looking for action handler if the component has actions declared, but current action is not among them
          if ((parent.actions instanceof FilteredActions) && !parent.actions.hasAction(action)) break;

          if (parent.payload !== undefined) payload = parent.payload;
          if (parent[actionName]) res.unshift({ handler: parent, payload });

          parent = parent.$parent;
        }
        return res;
      }

      function emitEvent(self, emitData) {
        self.$emit(...emitData);
        let parent = self;
        while (parent != null) {
          if (parent.$options.name === 'DfForm' ||
            parent.$options.name === 'DfTable' ||
            parent.$options.name === 'FormLayout'
          ) {
            parent.$emit(...emitData);
            return;
          }
          parent = parent.$parent;
        }
      }

      async function asyncSome(arr, fun) {
        for (const e of arr) {
          // eslint-disable-next-line no-await-in-loop
          if (await fun(e)) return true;
        }
        return false;
      }

      let lastExecutedHandler;
      const handlers = [
        ...getHandlersWithPayload(this, actionDFName),
        ...getHandlersWithPayload(this, 'processActionsGeneric'),
      ];

      const actionHandled = await asyncSome(
        handlers,
        async (handler) => {
          lastExecutedHandler = handler;
          return (handler.handler[actionDFName] ??
            handler.handler.processActionsGeneric)(action, handler.payload, extraData);
        },
      );
      if (!actionHandled && lastExecutedHandler) {
        // means action wasn't handled but some handlers were executed, return first handler
        lastExecutedHandler = handlers.shift();
      }
      emitEvent(this, [
        'action-executed',
        { action, handler: lastExecutedHandler?.payload, extraData, actionHandled },
      ]);
    },
  },
};
</script>
