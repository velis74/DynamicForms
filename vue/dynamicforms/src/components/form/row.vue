<template>
  <v-row v-if="anyFieldVisible" align="end">
    <slot name="before-columns"/>
    <component
      :is="column.layoutFieldComponentName"
      v-for="(column, idx) in renderableColumns"
      :key="`${idx}${column.renderKey}`"
      v-bind="columnData!(column)"
      :style="column.colspan !== 1 ? { flex: column.colspan } : null"
    />
    <slot name="after-columns"/>
  </v-row>
</template>

<script lang="ts">
import { defineComponent, inject, PropType } from 'vue';

import FilteredActions from '../actions/filtered-actions';

import FormFieldType from './definitions/field';
import FormPayload from './definitions/form-payload';
import { Column } from './definitions/layout';
import FormFieldGroup from './field-group.vue';
import FormField from './form-field.vue';
import calculateVisibility from './inputs/conditional-visibility';

interface Props {
  columns: Array<Column>;
  errors: Record<string, any>;
  anyFieldVisible: boolean;
}

interface Injects {
  payload: FormPayload;
  actions: FilteredActions;
}

interface OwnMethodsAndComputed {
  renderableColumns: Column[];
  columnData: (col: any) => any;
}

export default defineComponent<Props & Partial<Injects & OwnMethodsAndComputed>>({
  name: 'FormRow',
  components: { FormField, FormFieldGroup },
  inject: ['actions', 'payload'],
  props: {
    columns: { type: Array as PropType<Array<Column>>, required: true },
    errors: { type: Object, default: () => ({}) },
    anyFieldVisible: { type: Boolean, required: true },
  } as const,
  setup() {
    const actions = inject<FilteredActions>('actions');
    const payload = inject<FormPayload>('payload');

    return { actions, payload };
  },
  computed: {
    renderableColumns() {
      // We return all fields that are not suppressed and not hidden
      return this.columns.filter(
        (col: FormFieldType) => (
          col.isVisible && calculateVisibility(this.payload as FormPayload, col.conditionalVisibility)
        ),
      );
    },
  },
  methods: {
    columnData(col: any) {
      return {
        field: col,
        title: col.title,
        errors: this.errors,
        actions: this.actions,
      };
    },
  },
});
</script>
