import type { App } from 'vue';

import Action, { defaultActionHandler } from './components/actions/action';
import FilteredActions from './components/actions/filtered-actions';
import DisplayMode from './components/classes/display-mode';
import FormPayload from './components/form/definitions/form-payload';
import FormLayout from './components/form/definitions/layout';
import DialogSize from './components/modal/definitions/dialog-size';
import dfModal from './components/modal/modal-view-api';
import TcolumnGeneric from './components/table/tcolumn-generic.vue';
import apiClient from './components/util/api-client';
import { gettext, interpolate } from './components/util/translations-mixin';
import * as VuetifyComponents from './components/vuetify';

export * from './components/api_consumer/index-temporary';
export {
  Action,
  defaultActionHandler,
  apiClient,
  dfModal,
  DialogSize,
  DisplayMode,
  FilteredActions,
  FormLayout,
  FormPayload,
  gettext,
  interpolate,
};

// Test
//Test
export interface DynamicFormsOptions {
  ui: 'vuetify',
}

const defaultOptions: DynamicFormsOptions = { ui: 'vuetify' };

const uiOptions: Array<string> = ['vuetify'];

export function createDynamicForms(options: DynamicFormsOptions = defaultOptions) {
  const ui = options.ui || 'vuetify';

  const install = (app: App) => {
    app.provide('$df$ApplicationTheme', ui);
    app.config.globalProperties.gettext = (value: string) => gettext(value);
    app.config.globalProperties.interpolate = (str: string, data: { [key: string]: any }) => interpolate(str, data);
    switch (ui) {
    case 'vuetify':
      // check if Vuetify is installed

      // import all global instances that we need for vuetify to work
      Object.entries(VuetifyComponents).map(([name, component]) => app.component(name, component));
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
