<template>
  <b-modal v-model="show">
    <template #modal-title>
      <slot name="title"/>
    </template>
    <slot name="body"/>
    <template #modal-footer>
      <slot name="actions"/>
    </template>
  </b-modal>
</template>

<script>
export default {
  name: 'BootstrapModal',
  data() { return { show: false }; },
};
</script>
