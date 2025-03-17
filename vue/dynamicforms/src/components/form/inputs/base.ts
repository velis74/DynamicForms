import { computed } from 'vue';

import FilteredActions from '../../actions/filtered-actions';
import FormField from '../definitions/field';

export interface BaseProps {
  field: FormField;
  actions: FilteredActions;
  errors: any;
  showLabelOrHelpText?: boolean;
  modelValue: any;
}

export interface BaseEmits {
  (e: 'update:modelValue', value: any): void;
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

  // we need BaseBinds type to specify type for hide-details.
  // Otherwise, we get error on build saying that hide-details is not string field.
  type BaseBinds = {
    label: any;
    'error-messages': any;
    'error-count': any;
    hint?: any;
    'persistent-hint': any;
    'hide-details'?: boolean | 'auto';
  };
  const baseBinds = computed((): BaseBinds => ({
    label: label.value,
    'error-messages': errorsList.value,
    'error-count': errorsDisplayCount.value + 10, // +10 so that it can show "rules" error messages
    hint: helpText.value,
    'persistent-hint': true,
    'hide-details': 'auto',
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
