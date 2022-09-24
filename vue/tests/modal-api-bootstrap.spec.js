// eslint-disable-next-line import/order
import { mount } from '@vue/test-utils';

// eslint-disable-next-line no-unused-vars
import { BootstrapVue } from 'bootstrap-vue';
import Vue from 'vue';

// import DialogSize from '../components/classes/dialog-size';
// eslint-disable-next-line camelcase
import * as BootstrapComponents from '../components/bootstrap';
// eslint-disable-next-line camelcase
import DialogSize from '../components/classes/dialog-size';
// eslint-disable-next-line camelcase
import modal_api_bootstrap from '../components/modal/modal-api-bootstrap';

Object.values(BootstrapComponents).map((component) => Vue.component(component.name, component));

Vue.use(BootstrapVue);

// eslint-disable-next-line no-undef
describe('DialogSize', () => {
  // eslint-disable-next-line no-undef
  it('Check if string matches enum', () => {
    // eslint-disable-next-line no-unused-vars
    const wrapper = mount(modal_api_bootstrap, { propsData: { options: { size: DialogSize.SMALL } } });
    expect(wrapper.vm.computedClass).toEqual('sm'); // return '';
  });
});
