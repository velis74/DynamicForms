/**
 * translations mixin provides utility functions that gettext will recognise
 */
export default {
  methods: {
    gettext(str) {
      return window.gettext ? window.gettext(str) : str;
    },
  },
};
