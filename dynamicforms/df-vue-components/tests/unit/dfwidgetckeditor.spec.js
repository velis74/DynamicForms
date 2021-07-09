import { shallowMount } from '@vue/test-utils';
import dfwidgetckeditor from '@/components/bootstrap/widget/dfwidgetckeditor.vue';

describe('dfwidgetckeditor.vue Test', () => {
  it('ckeditor', () => {
    // Test ckeditor
    const wrapper = shallowMount(dfwidgetckeditor, {
      propsData: {
        render_params: {},
      },
    });

    expect(wrapper.vm.$options.name).toMatch('widgetckeditor');
  });
});
