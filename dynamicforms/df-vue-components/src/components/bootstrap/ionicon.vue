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
        self.loaded_svg = window.cache_ionicon[name] = res.data.replace(/<title>.*<\/title>/i, '');
      });
    }
  },
  methods: {},
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
