<template>
  <div v-if="loaded_svg" :key="loaded_svg" v-html="loaded_svg"/>
</template>

<script>
import { noop } from 'lodash';

import apiClient from '../../apiClient';

export default {
  name: 'IonIcon',
  props: { name: { type: String, required: false, default: null } },
  data() {
    return {
      loaded_svg: '',
    };
  },
  watch: {
    name() {
      this.loaded_svg = '';
      this.loadSVG();
    },
  },
  mounted() {
    this.loadSVG();
  },
  methods: {
    loadSVG() {
      const name = this.name;
      if (!window.cache_ionicon) { window.cache_ionicon = {}; }
      if (!name) {
        noop();
      } else if (window.cache_ionicon[name]) {
        if (typeof window.cache_ionicon[name].then === 'function') {
          window.cache_ionicon[name].then((res) => { this.loaded_svg = res.data; });
          this.loaded_svg = '&hellip;';
          return;
        }
        this.loaded_svg = window.cache_ionicon[name];
      } else {
        this.loaded_svg = '&hellip;';
        window.cache_ionicon[name] = apiClient.get(`https://unpkg.com/ionicons@5.5.1/dist/svg/${name}.svg`);
        window.cache_ionicon[name].then((res) => {
          // eslint-disable-next-line no-multi-assign
          this.loaded_svg = window.cache_ionicon[name] = res.data.replace(/<title>.*<\/title>/i, '');
        });
      }
    },
  },
};
</script>

<style>
/* this selector is actually used within the SVG returned from the server */
/*noinspection CssUnusedSymbol,SpellCheckingInspection*/
.ionicon {
  display: inline-block;
  height:  1.5em;
}
</style>
