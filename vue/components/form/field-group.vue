<template>
  <v-col :class="cssClasses + columnClasses">
    <v-card>
      <v-card-title v-if="field.title">
        {{ field.title }}
      </v-card-title>
      <v-card-text>
        <df-form-layout
          :is="field.componentName"
          :layout="field.layout"
          :payload="formPayload"
          :actions="actions"
          :errors="errors"
        />
      </v-card-text>
      <v-card-actions v-if="field.footer">
        {{ field.footer }}
      </v-card-actions>
    </v-card>
  </v-col>
</template>
<script lang="ts">
import { defineComponent } from 'vue';

import ActionHandlerMixin from '../actions/action-handler-mixin';

import FormPayload from './definitions/form-payload';

export default /* #__PURE__ */ defineComponent({
  name: 'FormFieldGroup',
  mixins: [ActionHandlerMixin],
  inject: ['actions', 'payload'],
  props: {
    field: { type: Object, required: true },
    errors: { type: Object, required: true },
    showLabelOrHelpText: { type: Boolean, default: true },
    cssClasses: { type: String, default: 'col' },
  },
  data: () => ({ formPayload: {} as FormPayload }),
  computed: {
    columnClasses() {
      const classes = this.field.widthClasses;
      return classes ? ` ${classes} ` : '';
    },
  },
  watch: {
    formPayload: {
      handler(newValue: any, oldValue: any) {
        this.payload[this.field.name] = this.formPayload;

        this.dispatchAction(
          this.actions.valueChanged,
          { field: this.field.name, oldValue, newValue },
        );
      },
      deep: true,
    },
  },
  created() {
    this.formPayload = new FormPayload(this.payload[this.field.name] ?? {}, this.field.layout);
  },
});
</script>

<style>
label {
  margin-inline-end: .5em;
}
</style>
