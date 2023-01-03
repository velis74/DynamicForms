<template>
  <v-row v-if="anyFieldVisible" align="end">
    <slot name="before-columns"/>
    <FormField
      :is="column.layoutFieldComponentName"
      v-for="(column, idx) in renderableColumns"
      :key="`${idx}${column.renderKey}`"
      :field="column"
      :payload="payload"
      :errors="errors"
    />
    <slot name="after-columns"/>
  </v-row>
</template>

<script lang="ts">
import { defineComponent } from 'vue';

import FormPayload from './definitions/form-payload';
import FormField from './field.vue';

export default defineComponent({
  name: 'FormRow',
  components: { FormField },
  props: {
    columns: { type: Array, required: true },
    payload: { type: FormPayload, default: null },
    errors: { type: Object, default: () => {} },
    anyFieldVisible: { type: Boolean, required: true },
  },
  computed: {
    renderableColumns() {
      // We return all fields that are not suppressed and not hidden
      return this.columns.filter((col: any) => col.isVisible);
    },
  },
});
</script>
