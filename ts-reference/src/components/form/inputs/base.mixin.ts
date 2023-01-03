import _ from 'lodash';
import { defineComponent } from 'vue';

import FilteredActions from '@/components/actions/filtered-actions';
import FormField from '@/components/form/definitions/field';


export default defineComponent({
  props: {
    field: { type: FormField, required: true },
    payload: { type: Object, required: true },
    actions: { type: FilteredActions, default: null },
    errors: { type: null, required: true },
    showLabelOrHelpText: { type: Boolean, default: true },
  },
  computed: {
    value: {
      get: function get() {
        return this.payload.value;
      },
      set: function set(newVal: any) {
        if (this.isNumber) {
          // TODO this is to be moved to input.vue. It has nothing to do here.
          if (this.isValidNumber(newVal)) {
            this.payload.setValue(Number(newVal));
            return;
          }
          this.payload.setValue(undefined);
          return;
        }
        this.payload.setValue(newVal);
      },
    },

    errorsList() { return this.errors || []; },
    errorsDisplayCount() { return this.errorsList.length; },
    label() { return this.showLabelOrHelpText ? this.field.label : null; },
    helpText() { return this.showLabelOrHelpText ? this.field.helpText : null; },
    baseBinds() {
      // this is potentially vuetify-specific
      return {
        label: this.label,
        'error-messages': this.errorsList,
        'error-count': this.errorsDisplayCount + 10, // +10 so that it can show "rules" error messages
        messages: this.helpText ? [this.helpText] : null,
      };
    },
    isNumber() {
      return this.field.renderParams.inputType === 'number';
    },
  },
  methods: {
    isValidNumber(num: number) {
      const notValidValues: Array<any> = [undefined, Number.NaN, ''];
      if (!this.field.allowNull) {
        notValidValues.push(null);
      }
      return !_.includes(notValidValues, num) && String(num) !== '' && !Number.isNaN(num) &&
        !_.includes(String(num), ',') && !_.endsWith(String(num), ',');
    },
  },
});
