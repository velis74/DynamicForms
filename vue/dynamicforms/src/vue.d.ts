declare module '@vue/runtime-core' {
  interface ComponentCustomProperties {
    gettext: (value: string) => string;
    interpolate: (str: string, data: { [key: string]: any }) => string;
  }
}

export {};
