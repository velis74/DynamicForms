/**
 * translations mixin provides utility functions that gettext will recognise
 */
declare global {
  interface Window {
    gettext?: (str: string) => string;
    interpolate?: (str: string, data: any[] | { [key: string]: any }, named: boolean) => string;
  }
}

function gettext(str: string): string {
  return window.gettext ? window.gettext(str) : str;
}

function interpolate(str: string, data: { [key: string]: any }): string {
  return window.interpolate ?
    window.interpolate(str, data, true) :
    str.replace(/%\(\w+\)s/g, (match) => String(data[match.slice(2, -2)]));
}

export { gettext, interpolate };

export default {
  methods: {
    gettext(str: string) { return gettext(str); },
    interpolate(str: string, data: { [key: string]: any }) { return interpolate(str, data); },
  },
};
