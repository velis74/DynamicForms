<template>
  <form :id="formUUID">
    <slot name="form-error"><div v-if="getErrorText"><small :id="'form-' + formUUID + '-err'"
                                   class="form-text text-danger">{{ getErrorText }}</small><hr></div></slot>
    <dfformrow v-for="(row, idx) in definition.rows" :key="idx" :columns="row" :data="record_data" :errors="errors"/>
  </form>
</template>

<script>
import dfformrow from '@/components/bootstrap/form/dfformrow.vue';
import eventBus from '@/logic/eventBus';

export default {
  name: 'dfformlayout',
  props: ['data', 'def', 'uuid', 'url'],
  mounted() {
    eventBus.$on(`formEvents_${this.formUUID}`, (payload) => {
      if (payload.type === 'submitErrors') {
        this.errors = payload.data;
      }
    });
  },
  data() {
    const definition = this.data.dialog || this.def;
    const formUUID = this.data.uuid || this.uuid;
    return {
      definition,
      formUUID,
      record_data: this.data.record || {},
      errors: {},
    };
  },
  computed: {
    getErrorText() {
      const nonFieldError = 'non_field_errors';
      try {
        if (this.errors && this.errors[nonFieldError]) return this.errors[nonFieldError];
        // eslint-disable-next-line no-empty
      } catch (e) {}
      return '';
    },
  },
  components: {
    dfformrow,
  },
  beforeDestroy() {
    eventBus.$off(`formEvents_${this.formUUID}`);
  },
};
</script>

<style scoped>

</style>
