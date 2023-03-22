<template>
  <v-col :class="cssClasses + columnClasses">
    <v-card>
      <v-card-title v-if="field.title">
        <span class="float-left pt-2">
          {{ field.title }}
        </span>
        <v-switch
          v-model="use"
          class="float-right"
          color="primary"
          density="compact"
        />
      </v-card-title>
      <v-expand-transition>
        <template v-if="use">
          <v-card-text>
            <df-form-layout
              :is="field.componentName"
              :layout="field.layout"
              :payload="formPayload"
              :actions="actions"
              :errors="errors"
              transition="scale-transition"
            />
          </v-card-text>
          <v-card-actions v-if="field.footer">
            {{ field.footer }}
          </v-card-actions>
        </template>
      </v-expand-transition>
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
  data: () => ({
    formPayload: new FormPayload(this.payload[this.field.name] ?? {}, this.field.layout) as FormPayload,
    use: !(this.payload[this.field.name] == null) as boolean,
  }),
  computed: {
    columnClasses() {
      const classes = this.field.widthClasses;
      return classes ? ` ${classes} ` : '';
    },
  },
  watch: {
    formPayload: {
      handler(newValue: Object, oldValue: Object) {
        // TODO: remove manual creation of recur field
        this.payload[this.field.name] = this.use ? {
          ...newValue,
          recur: { every: 2, weekdays: 1, holidays: 1, days: 1, dates: 1 },
        } : undefined;

        this.dispatchAction(
          this.actions.valueChanged,
          { field: this.field.name, oldValue, newValue },
        );
      },
      deep: true,
    },
    use: {
      handler(value: boolean) {
        this.payload[this.field.name] = value ? this.formPayload : undefined;
      },
    },
  },
});
</script>

<style>
label {
  margin-inline-end: .5em;
}
</style>
