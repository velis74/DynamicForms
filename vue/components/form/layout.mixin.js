import ActionHandlerMixin from '../actions/action-handler-mixin';
import FilteredActions from '../actions/filtered-actions';

import FormPayload from './definitions/form-payload';
import FormLayout from './definitions/layout';

export default {
  name: 'FormLayoutMixin',
  mixins: [ActionHandlerMixin], // TODO: implement also formFieldChangeMixin
  props: {
    layout: { type: FormLayout, required: true },
    payload: { type: FormPayload, default: null },
    actions: { type: FilteredActions, default: null },
    errors: { type: Object, default: () => {} },
  },
  computed: {
    nonFieldErrors() {
      const nonFieldError = 'non_field_errors';
      try {
        if (this.errors && this.errors[nonFieldError]) return this.errors[nonFieldError];
        // eslint-disable-next-line no-empty
      } catch (e) {}
      return '';
    },
  },
  mounted() {
    // TODO: implement errors notifications
    // eventBus.$on(`formEvents_${this.uuid}`, (payload) => {
    //   if (payload.type === 'submitErrors') {
    //     this.errors = payload.data;
    //   }
    // });
  },
  beforeDestroy() {
    // eventBus.$off(`formEvents_${this.uuid}`);
  },
};
