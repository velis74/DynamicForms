import type { App } from 'vue';

import * as apiconsumer from './components/api_consumer/index-temporary';
import TcolumnGeneric from './components/table/tcolumn-generic.vue';
import * as VuetifyComponents from './components/vuetify';
import VuetifyViewMode from './demo-app/vuetify/view-mode.vue';
import VuetifyApp from './demo-app/vuetify/vuetify-app.vue';

export { apiconsumer };

function unifyName(theme: string, name: string) {
  if (!name.toLowerCase().startsWith(theme.toLowerCase())) {
    if (name === 'LoadingIndicator' || name === 'DfModal') {
      // LoadingIndicator is a special case because it is not CSS framework dependent
      // dfModal is also not: instead it instantiates a DfModalDialog, which is CSS framework dependent
      return name;
    }
    console.error(`Error registering themed component ${name}. Should start with ${theme}, but does not!`);
  }
  return `Df${name.substring(theme.length)}`;
}

export interface DynamicFormsOptions {
  ui: 'vuetify',
}

const defaultOptions: DynamicFormsOptions = { ui: 'vuetify' };

const uiOptions: Array<string> = ['vuetify'];

export default function createDynamicForms(options: DynamicFormsOptions = defaultOptions) {
  const ui = options.ui || 'vuetify';

  const install = (app: App) => {
    app.provide('$df$ApplicationTheme', ui);
    switch (ui) {
    case 'vuetify':
      // check if Vuetify is installed

      // import all global instances that we need for vuetify to work
      app.component(unifyName(ui, VuetifyApp.name), VuetifyApp);
      app.component(unifyName(ui, VuetifyViewMode.name), VuetifyViewMode);
      Object.values(VuetifyComponents).map((component) => app.component(unifyName(ui, component.name), component));
      break;
    default:
      // issue a warning stating what are appropriate options
      throw new TypeError(`UI "${ui}" is not a valid option. Valid options are [${uiOptions.join(' ')}].`);
    }
    // common global components
    app.component(TcolumnGeneric.name, TcolumnGeneric);
  };

  return {
    install,
    ui,
  };
}
