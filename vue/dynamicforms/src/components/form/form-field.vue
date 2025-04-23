<script setup lang="ts">
import { debounce } from 'lodash-es';
import { computed, inject, ref, Ref, watch } from 'vue';

import { useActionHandler } from '../actions/action-handler-composable';
import FilteredActions from '../actions/filtered-actions';
import type { ActionsNS } from '../actions/namespace';

import FormField from './definitions/field';
import FormPayload from './definitions/form-payload';
import DDateTime from './inputs/date-time.vue';
import DCheckbox from './inputs/df-checkbox.vue';
import DCKEditor from './inputs/df-ckeditor.vue';
import DColor from './inputs/df-color.vue';
import DFile from './inputs/df-file.vue';
import DInput from './inputs/df-input.vue';
import DList from './inputs/df-list.vue';
import DPlaceholder from './inputs/df-placeholder.vue';
import DSelect from './inputs/df-select.vue';
import DTextArea from './inputs/text-area.vue';

type IHandlers = ActionsNS.IHandlers;

interface Props {
  field: FormField
  actions: FilteredActions
  errors: any
  showLabelOrHelpText?: boolean
  cssClasses?: string;
  handlers?: IHandlers;
  dialogHandlers?: IHandlers;
}

const props = withDefaults(defineProps<Props>(), {
  cssClasses: 'col',
  showLabelOrHelpText: true,
  handlers: undefined,
  dialogHandlers: undefined,
});

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
  DColor,
  DDateTime,
  DFile,
  DInput,
  DList,
  DPlaceholder,
  DSelect,
  DTextArea,
};

const component = computed(() => components?.[props.field.componentName] ?? DInput);

const debounceHandler = debounce((newValue: any, oldValue: any) => {
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
  if ((newValue === null || newValue === undefined) &&
    (oldValue === null || oldValue === undefined)) {
    return; // Don't trigger the watch logic
  }
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
      :handlers="handlers"
      :dialog-handlers="dialogHandlers"
      @update:modelValueDisplay="updateModelValueDisplay"
    />
  </v-col>
</template>

<style>
label {
  margin-inline-end: .5em;
}
</style>
