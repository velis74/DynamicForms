import { computed } from 'vue';

import FilteredActions from '../../actions/filtered-actions';

import FormField from '../definitions/field';

export interface BaseProps {
    field: FormField
    actions: FilteredActions
    errors: any
    showLabelOrHelpText?: boolean
    modelValue: any
}

export interface BaseEmits {
    (e: 'update:modelValue', value: any): any
}

export const basePropsDefault = { showLabelOrHelpText: true };

export function useInputBase(props: BaseProps, emit: BaseEmits) {
  const value = computed({
    get(): any {
      return props.modelValue;
    },
    set(newValue: any) {
      emit('update:modelValue', newValue);
    },
  });

  const errorsList = computed(() => props.errors || []);

  const errorsDisplayCount = computed(() => errorsList.value.length);

  const label = computed(() => (props.showLabelOrHelpText ? props.field.label : ''));

  const helpText = computed(() => (props.showLabelOrHelpText ? props.field.helpText : ''));

  const baseBinds = computed(() => ({
    label: label.value,
    'error-messages': errorsList.value,
    'error-count': errorsDisplayCount.value + 10, // +10 so that it can show "rules" error messages
    messages: helpText.value ? [helpText.value] : [],
  }));

  return {
    value,
    errorsList,
    errorsDisplayCount,
    label,
    helpText,
    baseBinds,
  };
}
