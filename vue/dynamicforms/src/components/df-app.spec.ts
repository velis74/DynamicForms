// Import the mount function from @vue/test-utils
import { mount } from '@vue/test-utils';

import { createDynamicForms } from '../index';

// Import your component
import DfApp from './df-app.vue';

// Describe the test suite
describe('DfApp.vue', () => {
  const df = createDynamicForms();
  // Test case 1: Ensure the component renders correctly
  it('renders component with ModalView and main component slot', () => {
    // Mount your component (DfApp)
    const wrapper = mount(DfApp, {
      // You can customize props or provide slots as needed for your test
      // For example, you might use slots to provide content for the named slot
      slots: { default: '<div class="mock-main-component">Main Component Content</div>' },
      global: { plugins: [df] },
    });

    // Assert that the ModalView is rendered
    expect(wrapper.findComponent({ name: 'ModalView' }).exists()).toBe(true);

    // Assert that the main component slot is rendered
    expect(wrapper.find('.mock-main-component').exists()).toBe(true);
    expect(wrapper.find('.mock-main-component').text()).toBe('Main Component Content');
  });

  // Test case 2: Add another component to the slot and check if it's rendered
  it('renders additional component in the main component slot', () => {
    // Mount your component with a different slot content
    const wrapper = mount(DfApp, {
      slots: { default: '<div class="another-component">Another Component Content</div>' },
      global: { plugins: [df] },
    });

    // Assert that the additional component in the slot is rendered
    expect(wrapper.find('.another-component').exists()).toBe(true);
    expect(wrapper.find('.another-component').text()).toBe('Another Component Content');
  });
});
