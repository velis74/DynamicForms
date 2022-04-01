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
  computed: { // eslint-disable-line object-curly-newline
    unitVisible() {
      // TODO: Looks like layout.fields.unit.visibility is not reactive... It doesn't update when you call setVisibility
      //  hence method unitVisibleMethod().
      return this.layout.fields.unit.visibility === DisplayMode.FULL;
    },
  },
  watch: { // eslint-disable-line object-curly-newline
    // Watching variables is one way of catering for dynamic field visibility / initialisation
    //   The other would be to track value-changed events emitted by the Layout. See valueChanged handler below

    // eslint-disable-next-line func-names
    'payload.note': function (newValue, oldValue) { this.noteChanged(newValue, oldValue); },
    payload: {
      handler(newValue) {
        // See note in handler funcion on https://vuejs.org/guide/essentials/watchers.html#deep-watchers
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
    unitVisibleMethod() {
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
      let intVisibility = this.unitVisibleMethod();
      let qtyVisibility = this.unitVisibleMethod();
      let cstVisibility = this.unitVisibleMethod();
      if (this.unitVisibleMethod()) {
        intVisibility = ['pcs', 'cst'].includes(newValue);
        qtyVisibility = newValue === 'wt';
        cstVisibility = newValue === 'cst';
      }

      // If you call setVisibility on field you are currently on it looses focus. Even if visibility didn't change.
      if (this.layout.fields.int_fld.isVisible !== intVisibility) {
        this.layout.fields.int_fld.setVisibility(intVisibility);
      }
      if (this.layout.fields.qty_fld.isVisible !== qtyVisibility) {
        this.layout.fields.qty_fld.setVisibility(qtyVisibility);
      }
      if (this.layout.fields.cst_fld.isVisible !== cstVisibility) {
        this.layout.fields.cst_fld.setVisibility(cstVisibility);
      }
    },
  },
};
</script>
