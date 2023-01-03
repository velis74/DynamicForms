/**
 * translations mixin provides utility functions that gettext will recognise
 */
import { defineComponent } from 'vue';

export default defineComponent({
  methods: {
    gettext(str: string) {
      return window.gettext ? window.gettext(str) : str;
    },
  },
});
