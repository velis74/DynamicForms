import { createApp } from 'vue';
import { createVuetify } from 'vuetify';

import createDynamicForms from '../../dynamicforms';

describe('Initialization Tests', () => {
  it('Create DynamicForms', () => {
    // test default configuration
    expect(createDynamicForms()).not.toBeNull();
    // test vuetify configuration
    expect(createDynamicForms({ ui: 'vuetify' })).not.toBeNull();
    // test wrong configuration
    // @ts-ignore
    expect(createDynamicForms({ ui: 'some-unknown-interface' })).toThrow(TypeError);
  });

  it('Hook DynamicForms to empty Create App', () => {
    const app = createApp({});
    const dynamicForms = createDynamicForms();
    expect(app.use(dynamicForms)).not.toBeNull();
  });

  it('Hook DynamicForms on an App that has Vuetify installed', () => {
    const app = createApp({});
    app.use(createVuetify());
    expect(app.use(createDynamicForms())).not.toBeNull();
  });
});
