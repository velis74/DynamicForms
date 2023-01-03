import { defineComponent } from 'vue';

import ActionHandlerMixin from '@/components/actions/action-handler.mixin';
import FilteredActions from '@/components/actions/filtered-actions';

import FormPayload from '@/components/form/definitions/form-payload';
import FormLayout from '@/components/form/definitions/layout';

export default defineComponent({
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
  beforeUnmount() {
    // eventBus.$off(`formEvents_${this.uuid}`);
  },
});
