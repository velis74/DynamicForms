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
import _ from 'lodash';

import FormPayload from './definitions/form_payload';
import FormLayout from './definitions/layout';
import FormRow from './row';

export default {
  name: 'FormLayout',
  components: { FormRow },
  // mixins: [formFieldChangeMixin], // TODO: implement
  props: {
    layout: { type: FormLayout, required: true },
    payload: { type: FormPayload, default: null },
  },
  data() { return { errors: {} }; },
  computed: {
    parentLayout() {
      let layout = this.$parent;
      while (layout && layout.$options.name !== 'FormLayout') layout = layout.$parent;
      return layout;
    },
    errorText() {
      const nonFieldError = 'non_field_errors';
      try {
        if (this.errors && this.errors[nonFieldError]) return this.errors[nonFieldError];
        // eslint-disable-next-line no-empty
      } catch (e) {}
      return '';
    },
  },
  mounted() {
    // TODO: implement errors notifications
    // eventBus.$on(`formEvents_${this.uuid}`, (payload) => {
    //   if (payload.type === 'submitErrors') {
    //     this.errors = payload.data;
    //   }
    // });
  },
  beforeDestroy() {
    // eventBus.$off(`formEvents_${this.uuid}`);
  },
  methods: {
    emit(eventName, eventData) {
      this.$emit(eventName, eventData);
      if (this.parentLayout) {
        const oldValue = _.cloneDeep(this.payload);
        oldValue[eventData.field] = eventData.oldValue;
        this.parentLayout.emit('value-changed', { field: this.layout.fieldName, oldValue, newValue: this.payload });
      }
    },
  },
};
</script>
