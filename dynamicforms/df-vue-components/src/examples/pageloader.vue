<template>
  <div :is="component" v-if="config" :key="config.uuid" :config="config"/>
</template>

<script>
import apiClient from '../apiClient';
import DFFormLayout from '../components/bootstrap/form/dfformlayout.vue';
import DFTable from '../components/dftable.vue';

export default {
  name: 'PageLoader',
  components: {
    DFTable, DFFormLayout,
  },
  emits: ['title-change', 'load-route'],
  data() {
    return {
      url: null,
      component: 'DFTable',
      config: null,
    };
  },
  watch: {
    $route(to) { this.goToRoute(to); },
  },
  mounted() {
    this.goToRoute(this.$route);
  },
  methods: {
    goToRoute(to) {
      // console.log(to);
      this.url = `${to.path}.component`;
      this.component = to.meta.component || 'DFTable';
      apiClient
        .get(this.url, {
          headers: { 'x-viewmode': 'TABLE_ROW', 'x-pagination': 1, 'x-df-render-type': 'component-def' },
        })
        .then((res) => {
          this.config = res.data;
          this.$emit('title-change', res.data.titles.table);
          this.$emit('load-route', to.path, res.data.uuid);
        })
        .catch((err) => {
          console.log(err);
          // eslint-disable-next-line no-alert
          alert(`Error retrieving component def:\n${err.data}`);
        });
    },
  },
};
</script>
