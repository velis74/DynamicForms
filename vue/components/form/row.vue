<template>
  <v-row align="end">
    <slot name="before-columns"/>
    <FormField
      :is="column.layoutFieldComponentName"
      v-for="(column, idx) in renderableColumns"
      :key="idx"
      :field="column"
      :payload="payload"
      :errors="errors"
    />
    <slot name="after-columns"/>
  </v-row>
</template>

<script>
import FormPayload from './definitions/form_payload';
import FormField from './field';

export default {
  name: 'FormRow',
  components: { FormField },
  props: {
    columns: { type: Array, required: true },
    payload: { type: FormPayload, default: null },
    errors: { type: Object, default: () => {} },
  },
  computed: {
    renderableColumns() {
      // We return all fields that are not suppressed and not hidden
      return this.columns.filter((col) => col.isVisible);
    },
  },
};
</script>

<style scoped>

</style>
