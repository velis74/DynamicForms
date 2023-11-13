<script setup lang="ts">
import _ from 'lodash';
import { computed, inject, ref, Ref, watch } from 'vue';

import { useActionHandler } from '../actions/action-handler-composable';
import FilteredActions from '../actions/filtered-actions';

import FormField from './definitions/field';
import FormPayload from './definitions/form-payload';
import DCheckbox from './inputs/checkbox.vue';
import DCKEditor from './inputs/df-ckeditor.vue';
import DDateTime from './inputs/datetime.vue';
import DFile from './inputs/file.vue';
import DInput from './inputs/input.vue';
import DList from './inputs/list.vue';
import DPlaceholder from './inputs/placeholder.vue';
import DSelect from './inputs/select.vue';
import DTextArea from './inputs/text-area.vue';

interface Props {
  field: FormField
  actions: FilteredActions
  errors: any
  showLabelOrHelpText?: boolean
  cssClasses?: string
}

const props = withDefaults(defineProps<Props>(), { cssClasses: 'col', showLabelOrHelpText: true });

const { callHandler } = useActionHandler();
const payload = inject<Ref<FormPayload>>('payload', ref({}) as Ref<FormPayload>);

const columnClasses = computed<string>(() => {
  const classes = props.field.widthClasses;
  return classes ? ` ${classes}` : '';
});

const fieldValue = computed({
  get(): any {
    return payload.value[props.field.name];
  },
  set(value: any) {
    payload.value[props.field.name] = value;
  },
});

const components: { [key: string]: any } = {
  DCheckbox,
  DCKEditor,
  DDateTime,
  DFile,
  DInput,
  DList,
  DPlaceholder,
  DSelect,
  DTextArea,
};

const component = computed(() => components?.[props.field.componentName] ?? DInput);

const debounceHandler = _.debounce((newValue: any, oldValue: any) => {
  callHandler(
    props.actions.valueChanged,
    { field: props.field.name, oldValue, newValue },
  );
}, 600);

const updateModelValueDisplay = (newValue: any) => {
  const fieldName = `${props.field.name}-display`;
  if (
    payload.value[fieldName] === undefined ||
    (Object.getOwnPropertyDescriptor(payload.value, fieldName)?.writable)
  ) {
    payload.value[fieldName] = newValue;
  }
};

watch(fieldValue, (newValue: any, oldValue: any) => {
  debounceHandler(newValue, oldValue);
});
</script>

<template>
  <v-col :class="cssClasses + columnClasses">
    <component
      :is="component"
      v-model="fieldValue"
      :field="field"
      :actions="actions"
      :errors="errors && errors[field.name]"
      :show-label-or-help-text="showLabelOrHelpText"
      @update:modelValueDisplay="updateModelValueDisplay"
    />
  </v-col>
</template>

<style>
label {
  margin-inline-end: .5em;
}
</style>
