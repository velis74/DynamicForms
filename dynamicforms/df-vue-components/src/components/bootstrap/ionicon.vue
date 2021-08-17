<template>
  <div :key="loaded_svg" v-if="loaded_svg" v-html="loaded_svg"></div>
</template>

<script>
import apiClient from '@/apiClient';
import { noop } from 'lodash';

export default {
  name: 'ionicon',
  props: ['name'],
  data() {
    return {
      loaded_svg: '',
    };
  },
  computed: {},
  mounted() {
    const self = this;
    const name = self.name;
    if (!window.cache_ionicon) { window.cache_ionicon = {}; }
    if (!name) {
      noop();
    } else if (window.cache_ionicon[name]) {
      if (typeof window.cache_ionicon[name].then === 'function') {
        window.cache_ionicon[name].then((res) => { self.loaded_svg = res.data; });
        self.loaded_svg = '&hellip;';
        return;
      }
      self.loaded_svg = window.cache_ionicon[name];
    } else {
      self.loaded_svg = '&hellip;';
      window.cache_ionicon[name] = apiClient.get(`https://unpkg.com/ionicons@5.5.1/dist/svg/${name}.svg`);
      window.cache_ionicon[name].then((res) => {
        // eslint-disable-next-line no-multi-assign
        self.loaded_svg = window.cache_ionicon[name] = res.data;
      });
    }
  },
  methods: {},
};
</script>

<style>
.ionicon {
  display: inline-block;
  height:  1.5em;
}
</style>
