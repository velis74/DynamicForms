import type { App } from 'vue'

import * as apiconsumer from './components/api_consumer/index-temporary';
import TcolumnGeneric from "./components/table/tcolumn-generic.vue";
import * as VuetifyComponents from "./components/vuetify";

import VuetifyApp from './demo-app/vuetify/vuetify-app.vue';
import VuetifyViewMode from './demo-app/vuetify/view-mode.vue';

export { apiconsumer };

export interface DynamicFormsOptions {
  ui: 'vuetify',
}

const defaultOptions: DynamicFormsOptions = { ui: 'vuetify' }

const uiOptions: Array<string> = [ 'vuetify' ];

export default function createDynamicForms(options: DynamicFormsOptions = defaultOptions) {
  const ui = options.ui || 'vuetify';

  const install = (app: App) => {
    switch (ui) {
      case 'vuetify':
        // check if Vuetify is installed

        // import all global instances that we need for vuetify to work
        app.component(VuetifyApp.name, VuetifyApp);
        app.component(VuetifyViewMode.name, VuetifyViewMode);
        Object.values(VuetifyComponents).map((component) => app.component(component.name, component));
        break;
      default:
        // issue a warning stating what are appropriate options
        throw new TypeError(`UI "${ui}" is not a valid option. Valid options are [${uiOptions.join(' ')}].`)
    }
    // common global components
    app.component(TcolumnGeneric.name, TcolumnGeneric);
  }

  return {
    install,
    ui
  };
}
