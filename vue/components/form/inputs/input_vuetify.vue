<template>
  <div>
    <label v-if="config.label">{{ config.label }}</label>
    <v-input v-bind="vInputConfig">
      <slot/>
    </v-input>
  </div>
</template>

<script>
import _ from 'lodash';

export default {
  name: 'VuetifyInput',
  props: { config: { required: true, type: Object } },
  computed: {
    vInputConfig() {
      return _.omit(this.config, ['label']);
    },
  },
};
</script>

<style scoped>

</style>
