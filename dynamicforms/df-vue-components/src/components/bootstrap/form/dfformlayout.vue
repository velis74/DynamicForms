<template>
  <form :id="uuid">
    <slot name="form-error"><div v-if="getErrorText"><small :id="'form-' + uuid + '-err'"
                                   class="form-text text-danger">{{ getErrorText }}</small><hr></div></slot>
    <dfformrow v-for="(row, idx) in rows" :key="idx" :columns="row" :data="record" :errors="errors"/>
  </form>
</template>

<script>
import dfformrow from './dfformrow.vue';
import eventBus from '../../../logic/eventBus';

export default {
  name: 'dfformlayout',
  props: { rows: {}, uuid: {}, record: { default: null } },
  mounted() {
    eventBus.$on(`formEvents_${this.uuid}`, (payload) => {
      if (payload.type === 'submitErrors') {
        this.errors = payload.data;
      }
    });
  },
  data() {
    return {
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
    eventBus.$off(`formEvents_${this.uuid}`);
  },
};
</script>

<style scoped>

</style>
