<template>
  <v-col :class="cssClasses + columnClasses">
    <component
      :is="field.componentName"
      v-model="fieldValue"
      :field="field"
      :actions="actions"
      :errors="errors && errors[field.name]"
      :show-label-or-help-text="showLabelOrHelpText"
      @update:modelValueDisplay="updateModelValueDisplay"
    />
  </v-col>
</template>

<script lang="ts">
import _ from 'lodash';
import { defineComponent, inject } from 'vue';

import { useActionHandler } from '../actions/action-handler-composable';
import ActionHandlerMixin from '../actions/action-handler-mixin';
import FilteredActions from '../actions/filtered-actions';

import FormField from './definitions/field';
import FormPayload from './definitions/form-payload';
import DCheckbox from './inputs/checkbox.vue';
import DCKEditor from './inputs/ckeditor.vue';
import DDateTime from './inputs/datetime.vue';
import DFile from './inputs/file.vue';
import DInput from './inputs/input.vue';
import DList from './inputs/list.vue';
import DPlaceholder from './inputs/placeholder.vue';
import DSelect from './inputs/select.vue';
import DTextArea from './inputs/text-area.vue';

export default /* #__PURE__ */ defineComponent({
  name: 'FormField',
  components: {
    DCheckbox,
    DCKEditor,
    DDateTime,
    DFile,
    DInput,
    DList,
    DPassword: DInput,
    DPlaceholder,
    DSelect,
    DTextArea,
  },
  mixins: [ActionHandlerMixin],
  props: {
    field: { type: FormField, required: true },
    actions: { type: FilteredActions, required: true },
    errors: { type: Object, required: true },
    showLabelOrHelpText: { type: Boolean, default: true },
    cssClasses: { type: String, default: 'col' },
  },
  setup() {
    const { callHandler } = useActionHandler();
    return { callHandler, payload: inject<FormPayload>('payload', {} as FormPayload) };
  },
  computed: {
    columnClasses(): string {
      const classes = this.field.widthClasses;
      return classes ? ` ${classes}` : '';
    },
    fieldValue: {
      get(): any { return this.payload[this.field.name]; },
      set(value: any) {
        this.payload[this.field.name] = value;
      },
    },
  },
  watch: {
    fieldValue: {
      handler(newValue: any, oldValue: any) {
        this.debounceHandler(this, newValue, oldValue);
      },
      // in case there are nested values in the future
      deep: true,
    },
  },
  methods: {
    updateModelValueDisplay(newValue: any) {
      const fieldName = `${this.field.name}-display`;
      if (Object.getOwnPropertyDescriptor(this.payload, fieldName)?.writable) {
        this.payload[fieldName] = newValue;
      }
    },
    debounceHandler: _.debounce((self, newValue, oldValue) => {
      self.callHandler(
        self.actions.valueChanged,
        { field: self.field.name, oldValue, newValue },
      );
    }, 600),
  },
});
</script>

<style>
label {
  margin-inline-end: .5em;
}
</style>
