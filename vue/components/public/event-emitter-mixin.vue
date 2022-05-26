<script>
import _ from 'lodash';

export default {
  name: 'EventEmitterMixin',
  methods: {
    getHandler(functionName, getPayload = false) {
      let parent = this.$parent;
      let payload = null;
      while (parent && parent[functionName] === undefined) {
        parent = parent.$parent;
        if (parent && parent.payload !== undefined && !payload) {
          payload = parent.payload;
        }
      }
      if (getPayload) {
        return payload;
      }
      return parent;
    },
    getDispatchActionFunctionName(actionData) {
      return `action${_.startCase(_.toLower(actionData.name))}`;
    },
    dispatchAction(actionData) {
      /**
       * Action is handled by a specific function on a component. First parent component which has this function
       * defined executes this function with arguments actionData, payload. Payload is a computed variable, for payload
       * value, value of first parent component's payload computed value is taken if payload computed var is defined.
       *
       * Function name which executes action data is "calculated from actionData attributes."
       */

      const functionName = this.getDispatchActionFunctionName(actionData);
      const handler = this.getHandler(functionName);

      console.log(handler, actionData);

      if (handler && handler[functionName]) {
        handler[functionName](actionData, this.getHandler(functionName, true));
        return;
      }
      if (this[functionName]) {
        this[functionName](actionData, this.payload);
      }
    },
  },
};
</script>
