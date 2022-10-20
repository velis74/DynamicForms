import { createLocalVue, mount } from '@vue/test-utils';
import Vue from 'vue';
import Vuetify from 'vuetify';

import DialogSize from '../components/classes/dialog-size';
// eslint-disable-next-line camelcase
import modal_api_vuetify from '../components/modal/modal-api-vuetify';
import * as VuetifyComponents from '../components/vuetify';
import VuetifyViewMode from '../demo-app/vuetify/view-mode';

Object.values(VuetifyComponents).map((component) => Vue.component(component.name, component));
Vue.component(VuetifyViewMode.name, VuetifyViewMode);

Vue.use(Vuetify);
// const vuetify = new Vuetify({});

describe('DialogSize', () => {
  // eslint-disable-next-line no-unused-vars
  let vuetify;
  const localVue = createLocalVue({ vuetify: new Vuetify({}) });
  beforeEach(() => {
    vuetify = new Vuetify();
  });

  it('Check if string matches enum', () => {
    const wrapper = mount(modal_api_vuetify, { localVue, vuetify, propsData: { options: { size: DialogSize.SMALL } } });
    // console.log(wrapper.vm.computedWidth, 44, wrapper.vm.size, wrapper.vm.fullScreen);
    // vrnjen je prazen string
    expect(wrapper.vm.computedWidth).toBe(400); // return '';
  });
});