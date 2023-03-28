/**
 * translations mixin provides utility functions that gettext will recognise
 */
declare global {
  interface Window {
    gettext?: (str: string) => string;
  }
}

function gettext(str: string) {
  return window.gettext ? window.gettext(str) : str;
}

export { gettext };

export default { methods: { gettext(str: string) { return gettext(str); } } };
