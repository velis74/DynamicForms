<template>
  <v-form>
    <!-- we start with any form-level error messages, if there are any -->
    <slot name="form-error">
      <div v-if="errorText" class="alert alert-danger">
        <small class="text-danger">{{ errorText }}</small>
      </div>
    </slot>
    <template v-for="(row, idx) in layout.rows">
      <FormRow
        :is="row.componentName"
        :key="`${idx}${row.renderKey}`"
        :columns="row.columns"
        :payload="payload"
        :errors="errors"
        :any-field-visible="row.anyVisible"
      />
    </template>
  </v-form>
</template>

<script>
import FormLayoutMixin from './layout.mixin';
import FormRow from './row';

export default {
  name: 'BootstrapFormLayout',
  components: { FormRow },
  mixins: [FormLayoutMixin],
};
</script>
