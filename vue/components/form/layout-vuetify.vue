<template>
  <v-form>
    <!-- we start with any form-level error messages, if there are any -->
    <slot name="form-error">
      <div v-if="nonFieldErrors">
        <!-- eslint-disable vue/require-v-for-key -->
        <template v-for="error in nonFieldErrors">
          <small class="red--text">{{ error }}</small>
        </template>
      </div>
    </slot>
    <!-- eslint-disable vue/no-v-for-template-key -->
    <template v-for="(row, idx) in layout.rows" :key="`${idx}${row.renderKey}`">
      <FormRow
        :is="row.componentName"
        :columns="row.columns"
        :errors="errors"
        :any-field-visible="row.anyVisible"
      />
    </template>
  </v-form>
</template>
<script lang="ts">
import { defineComponent } from 'vue';

import LayoutMixin from './layout.mixin';
import FormRow from './row.vue';

export default /* #__PURE__ */ defineComponent({
  name: 'VuetifyFormLayout',
  components: { FormRow },
  mixins: [LayoutMixin],
});
</script>
