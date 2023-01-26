<template>
  <v-col :class="cssClasses + columnClasses">
    <component
      :is="field.componentName"
      :field="field"
      :actions="actions"
      :payload="proceduralPayload"
      :errors="errors && errors[field.name]"
      :show-label-or-help-text="showLabelOrHelpText"
    />
  </v-col>
</template>

<script lang="ts">
import _ from 'lodash';
import { defineComponent } from 'vue';

import ActionHandlerMixin from '../actions/action-handler-mixin.vue';
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
  props: {
    field: { type: Object, required: true },
    actions: { type: FilteredActions, required: true },
    payload: { type: FormPayload, required: true },
    errors: { type: Object, required: true },
    showLabelOrHelpText: { type: Boolean, default: true },
    cssClasses: { type: String, default: 'col' },
  },
  computed: {
    columnClasses() {
      const classes = this.field.widthClasses;
      return classes ? ` ${classes}` : '';
    },
    proceduralPayload() {
      const self = this;
      return {
        get value() { return _.cloneDeep(self.payload[self.field.name]); },
        setValue: function setValue(newValue) {
          const oldValue = _.cloneDeep(self.payload[self.field.name]);
          self.payload[`set${self.field.name}Value`](newValue);
          self.dispatchAction(
            self.actions.valueChanged,
            { field: self.field.name, oldValue, newValue: self.payload[self.field.name] },
          );
        },
      };
    },
  },
});
</script>

<style>
label {
  margin-inline-end: .5em;
}
</style>
