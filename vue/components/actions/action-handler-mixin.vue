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
    dispatchAction(action, extraData) {
      let actionDFName = `action${_.startCase(_.camelCase(_.toLower(action.name)))}`;

      function getHandlersWithPayload(self) {
        // first, if action has a specific handler specified, let's just return that and be done with it
        if (action.handlerWithPayload) return [action.handlerWithPayload];
        // WARNING: It is unlikely, but possible that a parent would handle the event, but not have a payload prop
        let parent = self;
        let payload = null; // for some reason "this" got lost on this line, so I replaced it with self
        const res = [];
        while (parent != null) {
          if (parent.payload !== undefined) payload = parent.payload;
          if (parent[actionDFName]) res.unshift({ handler: parent, payload });

          // stop looking for action handler if the component has actions declared, but current action is not among them
          // please note that placing the if here actually still considers the component as a possible handler even
          // though it clearly does not have the action declared.
          // however, modal-view-api relies on this particular "oversight" so that it can run processActionsGeneric()
          if ((parent.actions instanceof FilteredActions) && !parent.actions.hasAction(action)) break;

          parent = parent.$parent;
        }
        return res;
      }

      const handlers = getHandlersWithPayload(this);
      if (!handlers.some((handler) => (handler.handler[actionDFName](action, handler.payload, extraData)))) {
        const actualActionName = actionDFName;
        actionDFName = 'processActionsGeneric';
        const hndlrs = getHandlersWithPayload(this);
        if (!hndlrs.some((handler) => (handler.handler[actionDFName](action, handler.payload, extraData)))) {
          console.warn(
            `[unprocessed] Action ${this.$options.name}.${actualActionName}()`,
          );
        }
      }
    },
  },
};
</script>
