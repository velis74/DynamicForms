<template>
  <v-col :class="cssClasses + columnClasses">
    <component
      :is="field.componentName"
      :field="field"
      :payload="proceduralPayload"
      :errors="errors && errors[field.name]"
      :show-label-or-help-text="showLabelOrHelpText"
    />
  </v-col>
</template>

<script>
import _ from 'lodash';

import FormPayload from './definitions/form_payload';
import DCheckbox from './inputs/checkbox';
import DCKEditor from './inputs/ckeditor';
import DDateTime from './inputs/datetime';
import DFile from './inputs/file';
import DInput from './inputs/input';
import DPlaceholder from './inputs/placeholder';
import DSelect from './inputs/select';

export default {
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
  props: {
    field: { type: Object, required: true },
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
    layout() {
      let layout = this.$parent;
      while (layout && layout.$options.name !== 'FormLayout') layout = layout.$parent;
      return layout;
    },
    proceduralPayload() {
      const self = this;
      return {
        get value() { return self.payload[self.field.name]; },
        setValue: function setValue(newValue) {
          const oldValue = _.cloneDeep(self.payload);
          self.payload[`set${self.field.name}Value`](newValue);
          self.layout.emit('value-changed', { field: self.field.name, oldValue, newValue: self.payload });
        },
      };
    },
  },
};
</script>

<style>
label {
  margin-inline-end: .5em;
}
</style>
