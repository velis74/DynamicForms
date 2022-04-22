import { mount } from '@vue/test-utils';
import Vue from 'vue';
import Vuetify from 'vuetify';

import DialogSize from '../components/classes/dialog_size';
// eslint-disable-next-line camelcase
import modal_api_vuetify from '../components/modal/modal_api_vuetify';
import * as VuetifyComponents from '../components/vuetify';
import VuetifyViewMode from '../demo_app/vuetify/view_mode';

Object.values(VuetifyComponents).map((component) => Vue.component(component.name, component));
Vue.component(VuetifyViewMode.name, VuetifyViewMode);

Vue.use(Vuetify);
// const vuetify = new Vuetify({});

describe('DialogSize', () => {
  it('Check if string matches enum', () => {
    const wrapper = mount(modal_api_vuetify, { propsData: { options: { size: DialogSize.SMALL } } });
    // console.log(wrapper.vm.computedWidth, 44, wrapper.vm.size, wrapper.vm.fullScreen);
    // vrnjen je prazen string
    expect(wrapper.vm.computedWidth).toBe(400); // return '';
  });
});
