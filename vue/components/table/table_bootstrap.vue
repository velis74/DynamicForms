<template>
  <b-card>
    <b-card-header>{{ title }}</b-card-header>
    <b-card-body>
      <BootstrapTHead/>
      <BootstrapTBody/>
      <BootstrapTFoot/>
    </b-card-body>
  </b-card>
</template>
<script>
import Table from './table';

export default {
  name: 'BootstrapTable',
  mixins: [Table],
};
</script>
