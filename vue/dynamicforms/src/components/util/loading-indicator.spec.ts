import { mount } from '@vue/test-utils';

import LoadingIndicator from './loading_indicator.vue';

describe('LoadingIndicator.vue', () => {
  it('renders loading state without progress', () => {
    const wrapper = mount(LoadingIndicator, { propsData: { loading: true } });

    expect(wrapper.find('.lds-ellipsis').exists()).toBe(true);
    expect(wrapper.find('.progress').exists()).toBe(false);
  });

  it('renders loading state with progress', () => {
    const wrapper = mount(LoadingIndicator, {
      propsData: {
        loading: true,
        progress: 30,
        label: 'Loading...',
      },
    });

    expect(wrapper.find('.lds-ellipsis').exists()).toBe(false);
    expect(wrapper.find('.progress').exists()).toBe(true);
    expect(wrapper.find('.progress-bar').attributes('aria-valuenow')).toBe('30');
    expect(wrapper.find('.progress-bar').text()).toContain('30%');
  });

  it('does not render if loading prop is false', () => {
    const wrapper = mount(LoadingIndicator, { propsData: { loading: false } });

    expect(wrapper.find('.progress-wrapper').exists()).toBe(false);
  });
});
