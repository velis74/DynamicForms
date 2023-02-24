<template>
  <v-col :class="cssClasses + columnClasses">
    <component
      :is="field.componentName"
      v-model="payload[this.field.name]"
      :field="field"
      :actions="actions"
      :errors="errors && errors[field.name]"
      :show-label-or-help-text="showLabelOrHelpText"
    />
  </v-col>
</template>

<script lang="ts">
import { defineComponent } from 'vue';

import ActionHandlerMixin from '../actions/action-handler-mixin';
import FilteredActions from '../actions/filtered-actions';

import FormPayload from './definitions/form-payload';
import DCheckbox from './inputs/checkbox.vue';
import DCKEditor from './inputs/ckeditor.vue';
import DDateTime from './inputs/datetime.vue';
import DFile from './inputs/file.vue';
import DInput from './inputs/input.vue';
import DPlaceholder from './inputs/placeholder.vue';
import DSelect from './inputs/select.vue';

export default /* #__PURE__ */ defineComponent({
  name: 'FormField',
  components: {
    DCheckbox,
    DCKEditor,
    DDateTime,
    DFile,
    DInput,
    DPassword: DInput,
    DPlaceholder,
    DSelect,
  },
  mixins: [ActionHandlerMixin],
  inject: { payload: { from: 'payload', default: {} as FormPayload } },
  props: {
    field: { type: Object, required: true },
    actions: { type: FilteredActions, required: true },
    errors: { type: Object, required: true },
    showLabelOrHelpText: { type: Boolean, default: true },
    cssClasses: { type: String, default: 'col' },
  },
  computed: {
    columnClasses() {
      const classes = this.field.widthClasses;
      return classes ? ` ${classes}` : '';
    },
    fieldValue() {
      return this.payload[this.field.name];
    },
  },
  watch: {
    fieldValue: {
      handler(newValue: any, oldValue: any) {
        this.dispatchAction(
          this.actions.valueChanged,
          { field: this.field.name, oldValue, newValue },
        );
      },
      // in case there are a nested value in the future
      deep: true,
    },
  },
});
</script>

<style>
label {
  margin-inline-end: .5em;
}
</style>
