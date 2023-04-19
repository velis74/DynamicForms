import type { App } from 'vue';

import Action, { defaultActionHandler } from './components/actions/action';
import FilteredActions from './components/actions/filtered-actions';
import DisplayMode from './components/classes/display-mode';
import FormPayload from './components/form/definitions/form-payload';
import DialogSize from './components/modal/dialog-size';
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
  FormPayload,
  gettext,
  interpolate,
};

function unifyName(theme: string, name: string) {
  if (!name.toLowerCase().startsWith(theme.toLowerCase())) {
    if (['LoadingIndicator', 'DfModal', 'ModalView'].includes(name)) {
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

export function createDynamicForms(options: DynamicFormsOptions = defaultOptions) {
  const ui = options.ui || 'vuetify';

  const install = (app: App) => {
    app.provide('$df$ApplicationTheme', ui);
    switch (ui) {
    case 'vuetify':
      // check if Vuetify is installed

      // import all global instances that we need for vuetify to work
      Object.values(VuetifyComponents).map((component) => {
        if (!component.name) console.warn('Component has no name', component);
        return app.component(unifyName(ui, component.name), component);
      });
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
