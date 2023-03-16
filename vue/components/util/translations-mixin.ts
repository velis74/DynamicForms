/**
 * translations mixin provides utility functions that gettext will recognise
 */
declare global {
  interface Window {
    gettext?: (str: string) => string;
  }
}

export default {
  methods: {
    gettext(str: string) {
      return window.gettext ? window.gettext(str) : str;
    },
  },
};
