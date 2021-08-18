<template>
  <div :is="component" v-if="config" :key="config.uuid" :config="config"/>
</template>

<script>
import dftable from '@/components/dftable.vue';
import formlayout from '@/components/bootstrap/form/dfformlayout.vue';
import axios from 'axios';

export default {
  name: 'pageloader',
  components: {
    dftable, formlayout,
  },
  data() {
    return {
      url: null,
      component: 'dftable',
      config: null,
    };
  },
  mounted() {
    this.goToRoute(this.$route);
  },
  methods: {
    goToRoute(to) {
      console.log(to);
      this.url = `http://localhost:8000${to.path}.component`;
      this.component = to.meta.component || 'dftable';
      axios
        .get(this.url, {
          headers: { 'x-viewmode': 'TABLE_ROW', 'x-pagination': 1, 'x-df-render-type': 'component-def' },
        })
        .then((res) => {
          this.config = res.data;
          this.$emit('title-change', res.data.titles.table);
        })
        .catch((err) => {
          console.log(err);
          // eslint-disable-next-line no-alert
          alert(`Error retrieving component def:\n${err.data}`);
        });
    },
  },
  watch: {
    $route(to) { this.goToRoute(to); },
  },
};
</script>
