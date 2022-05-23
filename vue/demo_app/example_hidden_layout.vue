<template>
  <FormLayout :layout="layout" :payload="payload" @value-changed="valueChanged"/>
</template>

<script>
import DisplayMode from '../components/classes/display_mode';
import FormPayload from '../components/form/definitions/form_payload';
import FormLayout from '../components/form/definitions/layout';

export default {
  name: 'ExampleHiddenLayout',
  props: {
    layout: { type: FormLayout, required: true },
    payload: { type: FormPayload, default: null },
  },
  data() {
    return { oldPayload: this.payload.deepClone() };
  },
  watch: { // eslint-disable-line object-curly-newline
    // Watching variables is one way of catering for dynamic field visibility / initialisation
    //   The other would be to track value-changed events emitted by the Layout. See valueChanged handler below

    // eslint-disable-next-line func-names
    'payload.note': function (newValue, oldValue) { this.noteChanged(newValue, oldValue); },
    payload: {
      handler(newValue) {
        // See note in handler function on https://vuejs.org/guide/essentials/watchers.html#deep-watchers
        // If we want to track changes we have to manually keep previous value in custom variable.
        this.unitChanged(newValue.unit);
        this.oldPayload = newValue.deepClone();
      },
      deep: true,
    },
  },
  mounted() { this.unitChanged(this.payload); },
  updated() { this.unitChanged(this.payload); },
  methods: {
    unitVisible() {
      return this.layout.fields.unit.visibility === DisplayMode.FULL;
    },
    valueChanged(payload) {
      // Tracking value-changed events emitted by the Layout is one of two ways of catering for dynamic field visibility
      //   Watching variables is another. See watch handler above
      if (payload.field === 'unit') this.unitChanged(payload.newValue.unit);
    },
    noteChanged(newValue) {
      this.layout.fields.unit.setVisibility(newValue !== 'abc');
      this.unitChanged(this.payload.unit);
    },
    unitChanged(newValue) {
      this.layout.fields.int_fld.setVisibility(this.unitVisible() && ['pcs', 'cst'].includes(newValue));
      this.layout.fields.qty_fld.setVisibility(this.unitVisible() && newValue === 'wt');
      this.layout.fields.cst_fld.setVisibility(this.unitVisible() && newValue === 'cst');
    },
  },
};
</script>
