import { DynamicFormsInputs, VuetifyComponents as vc } from '@dynamicforms/vuetify-inputs';
import Notifications from '@kyvg/vue3-notification';
import type { App } from 'vue';

import Action, { defaultActionHandler } from './components/actions/action';
import { useActionHandler } from './components/actions/action-handler-composable';
import FilteredActions from './components/actions/filtered-actions';
import type { DetailViewOptions } from './components/adapters/api/namespace';
import DisplayMode from './components/classes/display-mode';
import DfApp from './components/df-app.vue';
import FormPayload from './components/form/definitions/form-payload';
import FormLayout from './components/form/definitions/layout';
import DialogSize from './components/modal/definitions/dialog-size';
import dfModal from './components/modal/modal-view-api';
import AppNotification from './components/notifications/df-notifications.vue';
import RowTypes from './components/table/definitions/row-types';
import TColumnGeneric from './components/table/tcolumn-generic.vue';
import * as DfVuetifyComponents from './components/vuetify';
import * as VuetifyComponents from './vuetify-components';

import { apiClient, gettext, interpolate } from '@/util';

export * from './components/api_consumer/index-temporary';
export * from './components/api_consumer/form-consumer';
export * from './components/form/inputs/base';

export {
  Action,
  AppNotification,
  defaultActionHandler,
  apiClient,
  dfModal,
  DfApp,
  DialogSize,
  DisplayMode,
  FilteredActions,
  FormLayout,
  FormPayload,
  RowTypes,
  gettext,
  interpolate,
  useActionHandler,
  DetailViewOptions,
};

export interface DynamicFormsOptions {
  ui: 'vuetify',
}

export * as DfNotifications from './components/notifications/index';
const defaultOptions: DynamicFormsOptions = { ui: 'vuetify' };

const uiOptions: Array<string> = ['vuetify'];

export function createDynamicForms(options: DynamicFormsOptions = defaultOptions) {
  const ui = options.ui || 'vuetify';

  const install = (app: App) => {
    app.provide('$df$ApplicationTheme', ui);
    app.config.globalProperties.gettext = (value: string) => gettext(value);
    app.config.globalProperties.interpolate = (str: string, data: { [key: string]: any }) => interpolate(str, data);
    app.use(DynamicFormsInputs, { registerComponents: false, registerVuetifyComponents: false });
    app.use(Notifications);
    switch (ui) {
    case 'vuetify':
      // check if Vuetify is installed

      // import all global instances that we need for vuetify to work
      Object.entries({ ...VuetifyComponents, ...vc }).map(([name, component]) => app.component(name, component));
      Object.entries(DfVuetifyComponents).map(([name, component]) => app.component(name, component));
      app.component('DfApp', DfApp);
      break;
    default:
      // issue a warning stating what are appropriate options
      throw new TypeError(`UI "${ui}" is not a valid option. Valid options are [${uiOptions.join(' ')}].`);
    }
    // common global components
    app.component(TColumnGeneric.name!, TColumnGeneric);
  };

  return {
    install,
    ui,
  };
}
