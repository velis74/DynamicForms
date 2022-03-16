import FormField from '../definitions/field';

export default {
  props: {
    field: { type: FormField, required: true },
    payload: { type: Object, required: true },
    errors: { type: null, required: true },
    showLabelOrHelpText: { type: Boolean, default: true },
  },
  computed: {
    value: {
      get: function get() { return this.payload.value; },
      set: function set(newVal) { this.payload.setValue(newVal); },
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
  },
};
