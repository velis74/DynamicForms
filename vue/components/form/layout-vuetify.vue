<template>
  <v-form>
    <!-- we start with any form-level error messages, if there are any -->
    <slot name="form-error">
      <div v-if="errorText">
        <small class="red--text">{{ errorText }}</small>
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
import LayoutMixin from './layout.mixin';
import FormRow from './row';

export default {
  name: 'VuetifyFormLayout',
  components: { FormRow },
  mixins: [LayoutMixin],
};
</script>
