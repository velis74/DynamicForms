/**
 * translations mixin provides utility functions that gettext will recognise
 */

type InterpolateData = any[] | Record<string, any>;

declare global {
  interface Window {
    gettext?: (str: string) => string;
    interpolate?: (str: string, data: InterpolateData, named: boolean) => string;
  }
}

const gettext = (str: string) => (
  window.gettext ? window.gettext(str) : str
);

const interpolate = (str: string, data: Record<string, any>) => (
  window.interpolate ?
    window.interpolate(str, data, true) :
    str.replace(/%\(\w+\)s/g, (match) => String(data[match.slice(2, -2)]))
);

export function useTranslations() {
  return { gettext, interpolate };
}

export { gettext, interpolate };

export default {
  methods: {
    gettext(str: string) { return gettext(str); },
    interpolate(str: string, data: { [key: string]: any }) { return interpolate(str, data); },
  },
};
