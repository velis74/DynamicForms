import _ from 'lodash';
import { computed } from 'vue';

import FilteredActions from '../../actions/filtered-actions';
import FormField from '../definitions/field';

export interface BaseProps {

    field: FormField
    actions: FilteredActions
    errors: any
    showLabelOrHelpText: boolean
    modelValue: any
}

export interface BaseEmits {
    (e: 'update:modelValue', value: any): any
}

export function useInputBase(props: BaseProps, emit: BaseEmits) {
  const isNumber = computed(() => props.field.renderParams.inputType === 'number');
  function isValidNumber(num: any) {
    const notValidValues: any[] = [undefined, Number.NaN];
    if (!props.field.allowNull) {
      notValidValues.push(null);
      notValidValues.push('');
    }
    return !_.includes(notValidValues, num) && !Number.isNaN(num) &&
      !_.includes(String(num), ',') && !_.endsWith(String(num), ',');
    }

  const value = computed({
    get(): any {
      return props.modelValue;
    },
    set(newValue: any) {
      // TODO this is to be moved to input.vue. It has nothing to do here.
      if (isNumber.value && isValidNumber(newValue)) {
        emit('update:modelValue', newValue ? Number(newValue) : undefined);
        return;
      }
      emit('update:modelValue', newValue);
    },
  });

  const errorsList = computed(() => props.errors || []);

  const errorsDisplayCount = computed(() => errorsList.value.length);

  const label = computed(() => props.showLabelOrHelpText ? props.field.label : undefined);

  const helpText = computed(() => props.showLabelOrHelpText ? props.field.helpText : undefined);

  const baseBinds = computed(() => {
    // this is potentially vuetify-specific
    return {
      label: label.value,
      'error-messages': errorsList.value,
      'error-count': errorsDisplayCount.value + 10, // +10 so that it can show "rules" error messages
      messages: helpText.value ? [helpText.value] : undefined,
    };
  });
  return {
    value,
    errorsList,
    errorsDisplayCount,
    label,
    helpText,
    baseBinds,
    isNumber,
    isValidNumber,
  };
}
