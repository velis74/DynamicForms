<template>
  <div>
  <component :is="component + 'modal'"/>
  </div>
</template>

<script>
import bootstrapmodal from './bootstrap/modalhandler.vue';
// import JqueryuiTable from './jqueryui/Table.vue';

export default {
  name: 'modalhandler',
  computed: {
    component() {
      return window.dynamicformsUi;
    },
  },
  components: {
    bootstrapmodal,
    // JqueryuiTable,
  },
};
</script>

<style scoped>

</style>
