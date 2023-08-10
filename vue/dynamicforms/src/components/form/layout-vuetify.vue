<script setup lang="ts">
import { computed, ComputedRef, provide } from 'vue';

import { IHandlers, useActionHandler } from '../actions/action-handler-composable';
import FilteredActions from '../actions/filtered-actions';

import FormPayload from './definitions/form-payload';
import FormLayout from './definitions/layout';
import FormRow from './row.vue';

interface Props {
  layout: FormLayout
  payload?: FormPayload | null
  actions: FilteredActions
  actionHandlers?: IHandlers
  errors: { [key: string]: string[] }
}
const props = withDefaults(defineProps<Props>(), { payload: null, actionHandlers: undefined });

provide<FilteredActions>('actions', props.actions);
provide<ComputedRef<FormPayload | null>>('payload', computed(() => props.payload));

if (props.actionHandlers) {
  const { handler } = useActionHandler();
  Object.entries(props.actionHandlers).map(([name, fun]) => {
    handler.register(name, fun);
    return [name, fun];
  });
}

const nonFieldErrors = computed(() => {
  const nonFieldError = 'non_field_errors';
  if (props.errors?.[nonFieldError]) return props.errors[nonFieldError];
  return '';
});
</script>

<template>
  <v-form>
    <!-- we start with any form-level error messages, if there are any -->
    <slot name="form-error">
      <div v-if="nonFieldErrors" class="mb-8">
        <small
          v-for="error in nonFieldErrors"
          :key="error"
          class="text-error"
        >
          {{ error }}
        </small>
      </div>
    </slot>
    <FormRow
      :is="row.componentName"
      v-for="(row, idx) in layout.rows"
      :key="`${idx}${row.renderKey}`"
      :columns="row.columns"
      :errors="errors"
      :any-field-visible="row.anyVisible"
    />
  </v-form>
</template>
