<template>
  <form :id="uuid">
    <slot name="form-error">
      <div v-if="errorText" class="alert alert-danger">
        <small :id="'form-' + uuid + '-err'" class="text-danger">{{ errorText }}</small>
      </div>
    </slot>
    <DFFormRow v-for="(row, idx) in rows" :key="idx" :columns="row" :data="record" :errors="errors"/>
  </form>
</template>

<script>
import eventBus from '../../../logic/eventBus';
import formFieldChangeMixin from '../../../logic/formFieldChangeMixin';

import DFFormRow from './dfformrow.vue';

export default {
  name: 'DFFormLayout',
  components: { DFFormRow },
  mixins: [formFieldChangeMixin],
  props: {
    rows: { type: Array, required: true },
    uuid: { type: String, required: true },
    record: { type: Object, default: null },
  },
  data() {
    return {
      errors: {},
    };
  },
  computed: {
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
    eventBus.$on(`formEvents_${this.uuid}`, (payload) => {
      if (payload.type === 'submitErrors') {
        this.errors = payload.data;
      }
    });
  },
  beforeDestroy() {
    eventBus.$off(`formEvents_${this.uuid}`);
  },
};
</script>
