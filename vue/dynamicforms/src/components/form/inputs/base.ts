import Form, { Field, ValidationErrorRenderContent } from '@dynamicforms/vue-forms';
import { computed } from 'vue';

import FilteredActions from '../../actions/filtered-actions';
import FormField from '../definitions/field';

import type { ActionsNS } from '@/actions/namespace';

type IHandlers = ActionsNS.IHandlers;

export interface BaseProps {
  field: FormField;
  actions: FilteredActions;
  errors: any;
  showLabelOrHelpText?: boolean;
  modelValue: any;
  handlers?: IHandlers;
  dialogHandlers?: IHandlers;
}

export interface BaseEmits {
  (e: 'update:modelValue', value: any): void;
}

export const basePropsDefault = { showLabelOrHelpText: true, handlers: undefined, dialogHandlers: undefined };

export function useInputBase(props: BaseProps, emit: BaseEmits) {
  const value = computed({
    get(): any {
      return props.modelValue;
    },
    set(newValue: any) {
      emit('update:modelValue', newValue);
    },
  });

  const errorsList = computed(() => {
    if (props.errors != null) {
      if (props.errors instanceof Array) return props.errors;
      return [props.errors];
    }
    return [];
  });

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
    control?: Form.IField;
    placeholder: string;
    'persistent-placeholder': boolean;
    enabled?: boolean;
  };
  const control = computed(() => Field.create({
    value: value.value,
    touched: true,
    visibility: Form.DisplayMode.FULL,
    errors: (errorsList.value || []).map(
      (error: any) => (error instanceof ValidationErrorRenderContent ? error : new ValidationErrorRenderContent(error)),
    ),
    enabled: true,
  }));

  control.value.validate();

  const baseBinds = computed((): BaseBinds => ({
    label: label.value,
    'error-messages': errorsList.value,
    'error-count': errorsDisplayCount.value + 10, // +10 so that it can show "rules" error messages
    hint: helpText.value,
    'persistent-hint': true,
    'hide-details': 'auto',
    control: control.value,
    placeholder: props.field.placeholder,
    'persistent-placeholder': Boolean(props.field.placeholder && props.field.placeholder.length > 0),
    enabled: !props.field.readOnly,
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
