import _ from 'lodash';
import { defineComponent } from 'vue';

import FilteredActions from '../../actions/filtered-actions';
import FormField from '../definitions/field';

export default defineComponent({
  props: {
    field: { type: FormField, required: true },
    actions: { type: FilteredActions, required: true },
    errors: { type: null, required: true },
    showLabelOrHelpText: { type: Boolean, default: true },
    modelValue: { type: undefined, required: true },
  },
  emits: ['update:modelValue'],
  computed: {
    value: {
      get() { return this.modelValue; },
      set(newValue: any) {
        // TODO this is to be moved to input.vue. It has nothing to do here.
        if (this.isNumber && this.isValidNumber(newValue)) {
          this.$emit('update:modelValue', Number(newValue));
          return;
        }
        this.$emit('update:modelValue', newValue);
      },
    },

    errorsList() { return this.errors || []; },
    errorsDisplayCount() { return this.errorsList.length; },
    label() { return this.showLabelOrHelpText ? this.field.label : undefined; },
    helpText() { return this.showLabelOrHelpText ? this.field.helpText : undefined; },
    baseBinds() {
      // this is potentially vuetify-specific
      return {
        label: this.label,
        'error-messages': this.errorsList,
        'error-count': this.errorsDisplayCount + 10, // +10 so that it can show "rules" error messages
        messages: this.helpText ? [this.helpText] : undefined,
      };
    },
    isNumber() {
      return this.field.renderParams.inputType === 'number';
    },
  },
  methods: {
    isValidNumber(num: any) {
      const notValidValues: any[] = [undefined, Number.NaN];
      if (!this.field.allowNull) {
        notValidValues.push(null);
        notValidValues.push('');
      }
      return !_.includes(notValidValues, num) && !Number.isNaN(num) &&
        !_.includes(String(num), ',') && !_.endsWith(String(num), ',');
    },
  },
});
