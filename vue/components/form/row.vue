<template>
  <v-row v-if="anyFieldVisible" align="end">
    <slot name="before-columns"/>
    <component
      :is="column.layoutFieldComponentName"
      v-for="(column, idx) in renderableColumns"
      :key="`${idx}${column.renderKey}`"
      v-bind="columnData(column)"
    />
    <slot name="after-columns"/>
  </v-row>
</template>

<script lang="ts">
import { defineComponent } from 'vue';

import FormFieldGroup from './field-group.vue';
import FormField from './field.vue';

export default /* #__PURE__ */ defineComponent({
  name: 'FormRow',
  components: { FormField, FormFieldGroup },
  inject: ['actions', 'payload'],
  props: {
    columns: { type: Array, required: true },
    errors: { type: Object, default: () => {} },
    anyFieldVisible: { type: Boolean, required: true },
  },
  computed: {
    renderableColumns() {
      // We return all fields that are not suppressed and not hidden
      return this.columns.filter((col) => col.isVisible);
    },
  },
  methods: {
    columnData(col: any) {
      switch (col.layoutFieldComponentName) {
      case 'FormField':
        return {
          field: col,
          errors: this.errors,
          actions: this.actions,
        };
      case 'FormFieldGroup':
        return {
          field: col,
          title: col.title,
          errors: this.errors,
          actions: this.actions,
        };
      default:
        return {};
      }
    },
  },
});
</script>
