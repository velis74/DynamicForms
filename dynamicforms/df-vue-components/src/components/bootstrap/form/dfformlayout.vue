<template>
<form :id="'form-' + uuid">
    <dfformrow v-for="(row, idx) in definition.rows" :key="idx" :columns="row" :data="record_data"/>
  </form>
</template>

<script>
import dfformrow from '@/components/bootstrap/form/dfformrow.vue';

export default {
  name: 'formlayout',
  props: ['data', 'def', 'uuid', 'url'],
  data() {
    const definition = this.data.dialog || this.def;
    return {
      definition,
      record_data: definition.record_data || {},
    };
  },
  components: {
    dfformrow,
  },
};
</script>

<style scoped>

</style>
