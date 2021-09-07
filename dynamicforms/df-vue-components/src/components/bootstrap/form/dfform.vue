<template>
  <div class="card">
    <div class="card-header">{{ data.titles.edit }}</div>
    <div class="card-body">
      <DFFormLayout :rows="data.dialog.rows" :uuid="data.uuid"/>
    </div>
  </div>
</template>

<script>
// TODO: this file is completely redundant. It's basically just a card wrapper around DFFormLayout. It should be named
//  appropriately
import DFFormLayout from './dfformlayout.vue';

export default {
  name: 'DFForm',
  components: { DFFormLayout },
  props: {
    data: {
      type: Object,
      required: true,
      validator: (data) => (data.titles && data.titles.edit),
    },
  },
};
</script>

<style scoped>

</style>
