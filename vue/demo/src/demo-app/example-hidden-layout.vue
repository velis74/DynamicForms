<template>
  <df-form-layout :layout="layout" :payload="payload" :errors="errors"/>
</template>

<script lang="ts">
import { Action, DisplayMode, FormLayout, FormPayload } from 'dynamicforms';
import { defineComponent } from 'vue';

type ExtraDataType = {
  field: string,
  oldValue: any,
  newValue: any,
};

export default defineComponent({
  name: 'ExampleHiddenLayout',
  props: {
    layout: { type: FormLayout, required: true },
    payload: { type: FormPayload, default: null },
    errors: { type: Object, default: () => {} },
  },
  data() {
    return { oldPayload: new FormPayload({} as FormPayload) };
  },
  watch: {
    // Watching variables is one way of catering for dynamic field visibility / initialisation
    //   The other would be to track value-changed events emitted by the Layout. See valueChanged handler below

    // eslint-disable-next-line func-names
    'payload.note': function (newValue: string) { this.noteChanged(newValue); },
    payload: {
      handler(newValue: FormPayload) {
        // See note in handler function on https://vuejs.org/guide/essentials/watchers.html#deep-watchers
        // If we want to track changes we have to manually keep previous value in custom variable.
        this.unitChanged(newValue.unit);
        this.oldPayload = new FormPayload(newValue);
      },
      deep: true,
    },
  },
  mounted() { this.unitChanged(this.payload.unit); },
  updated() { this.unitChanged(this.payload.unit); },
  methods: {
    getVisibilityMode(mode: boolean): DisplayMode {
      return mode ? DisplayMode.FULL : DisplayMode.HIDDEN;
    },
    unitVisible(): boolean {
      return this.layout.fields.unit.visibility === DisplayMode.FULL;
    },
    actionValueChanged(action: Action, payload: FormPayload, extraData: ExtraDataType) {
      // Creating a value-changed handler is one of two ways of catering for dynamic field visibility
      //   Watching variables is another. See watch handler above
      //   Note that 'unit' will also be handled by the "payload" watch above
      if (extraData.field === 'unit') this.unitChanged(extraData.newValue);
    },
    noteChanged(newValue: string) {
      this.layout.fields.unit.setVisibility(newValue !== 'abc' ? DisplayMode.FULL : DisplayMode.HIDDEN);
      this.unitChanged(this.payload.unit);
    },
    unitChanged(newValue: string) {
      this.layout.fields.int_fld.setVisibility(
        this.getVisibilityMode(this.unitVisible() && ['pcs', 'cst'].includes(newValue)),
      );
      this.layout.fields.qty_fld.setVisibility(
        this.getVisibilityMode(this.unitVisible() && newValue === 'wt'),
      );
      this.layout.fields.cst_fld.setVisibility(
        this.getVisibilityMode(this.unitVisible() && newValue === 'cst'),
      );
    },
  },
});
</script>
