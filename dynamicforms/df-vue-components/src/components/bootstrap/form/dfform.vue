<template>
<div class="card">
    <div class="card-header">{{ data.titles.edit }}</div>
    <div class="card-body">
      <dfformlayout :rows="data.dialog.rows" :uuid="data.uuid"/>
    </div>
  </div>
</template>

<script>
import dfformlayout from '@/components/bootstrap/form/dfformlayout.vue';

export default {
  name: 'dfform',
  props: ['data'],
  components: {
    dfformlayout,
  },
};
</script>

<style scoped>

</style>
