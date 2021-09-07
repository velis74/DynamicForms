<template>
  <div>
    <component :is="component + 'Modal'"/>
  </div>
</template>

<script>
import DynamicForms from '../dynamicforms';

import BootstrapModal from './bootstrap/modalhandler.vue';

export default {
  name: 'ModalHandler',
  components: {
    BootstrapModal, // JQueryUIModal
  },
  computed: {
    component() {
      return DynamicForms.UI;
    },
  },
};
</script>

<style scoped>

</style>
