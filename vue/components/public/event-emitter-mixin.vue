<script>
import _ from 'lodash';

export default {
  name: 'EventEmitterMixin',
  methods: {
    getHandlerWithPayload(functionName) {
      let parent = this.$parent;
      let payload = null;
      while (parent && parent[functionName] === undefined) {
        parent = parent.$parent;
        if (parent && parent.payload !== undefined) {
          payload = parent.payload;
        }
      }
      return [parent, payload];
    },
    getDispatchActionFunctionName(actionData) {
      return `action${_.startCase(_.toLower(actionData.name))}`;
    },
    dispatchAction(actionData) {
      /**
       * Action is handled by a specific function on a component. First parent component which has this function
       * defined executes this function with arguments actionData, payload. Payload is a computed variable, for payload
       * value, value of first parent component's payload computed value is taken if payload computed var is defined.
       * If this function returns false then current component tries to exceute functionName(payload)
       *
       * Function name which executes action data is "calculated from actionData attributes."
       */

      const functionName = this.getDispatchActionFunctionName(actionData);
      const handlerAndPayload = this.getHandlerWithPayload(functionName);
      let payloadProcessedByHandler = false;
      if (handlerAndPayload[0] && handlerAndPayload[0][functionName]) {
        payloadProcessedByHandler = handlerAndPayload[0][functionName](actionData, handlerAndPayload[1]);
      }
      if (!payloadProcessedByHandler && this[functionName]) {
        this[functionName](actionData, this.payload);
      }
    },
  },
};
</script>
