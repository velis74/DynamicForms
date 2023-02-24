<template>
  <v-row v-if="anyFieldVisible" align="end">
    <slot name="before-columns"/>
    <FormField
      :is="column.layoutFieldComponentName"
      v-for="(column, idx) in renderableColumns"
      :key="`${idx}${column.renderKey}`"
      :field="column"
      :errors="errors"
      :actions="actions"
    />
    <slot name="after-columns"/>
  </v-row>
</template>

<script lang="ts">
import { defineComponent } from 'vue';

import FormField from './field.vue';

export default /* #__PURE__ */ defineComponent({
  name: 'FormRow',
  components: { FormField },
  inject: ['actions'],
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
});
</script>
