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
      const actionDFName = `action${_.startCase(_.camelCase(_.toLower(action.name)))}`;

      function getHandlersWithPayload(self) {
        // WARNING: It is unlikely, but possible that a parent would handle the event, but not have a payload prop
        let parent = self;
        let payload = null; // for some reason this got lost on this line, so I replaced it with self
        const res = [];
        while (parent != null) {
          if (parent.payload !== undefined) payload = parent.payload;
          if (parent[actionDFName]) res.unshift({ handler: parent, payload });

          if ((parent.actions instanceof FilteredActions) && !parent.actions.hasAction(action)) break;
          parent = parent.$parent;
        }
        return res;
      }

      const handlers = getHandlersWithPayload(this);
      if (!handlers.some((handler) => (handler.handler[actionDFName](action, handler.payload, extraData)))) {
        console.warn(
          `[unprocessed] Action ${this.$options.name}.${actionDFName}()`,
        );
      }
    },
  },
};
</script>
