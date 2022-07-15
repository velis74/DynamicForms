import { mount } from '@vue/test-utils';
import flushPromises from 'flush-promises';
import Vue from 'vue';
import Vuetify from 'vuetify';
import _ from 'lodash';

import VuetifyActions from '../components/actions/actions_vuetify';
import * as VuetifyComponents from '../components/vuetify';

Vue.use(Vuetify);
Object.values(VuetifyComponents)
  .map((component) => Vue.component(component.name, component));

jest.mock('axios', () => ({
  create: () => ({
    interceptors: {
      request: {
        use: () => {
        }
      }
    }
  }),
  get: async (url) => {
    console.warn('juhuhu');
    if (url.includes('failure')) throw new Error('bad url');
    return {
      data: '<svg xmlns="http://www.w3.org/2000/svg" class="ionicon" ' +
        'viewBox="0 0 512 512"><title>Warning</title><path d="M449.07 399.08L278.64 82.58c-12.08-22.44-44.26-22.44' +
        '-56.35 0L51.87 399.08A32 32 0 0080 446.25h340.89a32 32 0 0028.18-47.17zm-198.6-1.83a20 20 0 1120-20 20 20' +
        ' 0 01-20 20zm21.72-201.15l-5.74 122a16 16 0 01-32 0l-5.74-121.95a21.73 21.73 0 0121.5-22.69h.21a21.74 21.74' +
        ' 0 0121.73 22.7z"/></svg>',
    };
  },
}));

const actionsCopy = [
  {
    position: 'FILTER_ROW_END',
    field_name: null,
    name: 'add',
    // eslint-disable-next-line max-len
    action_js: 'dynamicforms.newRow(\'{% url url_reverse|add:\'-detail\' pk=\'new\' format=\'html\' %}\', \'record\', __TABLEID__);',
    action: null,
    label: '+ Add',
    title: 'Add new record',
    icon: 'add-outline',
    classes: null,
    displayStyle: {
      asButton: true,
      showLabel: true,
      showIcon: true,
      xs: {
        asButton: true,
        showLabel: false,
        showIcon: true,
      },
      md: {
        asButton: true,
        showLabel: true,
        showIcon: false,
      },
      lg: {
        asButton: true,
        showLabel: true,
        showIcon: true,
      },
    },
  },
  {
    position: 'ROW_CLICK',
    field_name: null,
    name: 'edit',
    // eslint-disable-next-line max-len
    action_js: 'dynamicforms.editRow(\'{% url url_reverse|add:\'-detail\' pk=\'__ROWID__\' format=\'html\' %}\'.replace(\'__ROWID__\', $(event.target.parentElement).closest(\'tr[class="df-table-row"]\').attr(\'data-id\')), \'record\', __TABLEID__);',
    action: null,
    label: 'Edit',
    title: 'Edit record',
    icon: 'edit-outline',
    classes: null,
    displayStyle: null,
  },
  {
    position: 'ROW_END',
    field_name: null,
    name: 'delete',
    // eslint-disable-next-line max-len
    action_js: 'dynamicforms.deleteRow(\'{% url url_reverse|add:\'-detail\' pk=row.id %}\', {{row.id}}, \'record\', __TABLEID__);',
    action: null,
    label: 'Delete',
    title: 'Delete record',
    icon: 'trash-outline',
    classes: null,
    displayStyle: {
      xs: {
        asButton: true,
        showLabel: true,
        showIcon: true,
      },
    },
  },
  {
    position: 'FILTER_ROW_END',
    field_name: null,
    name: 'filter',
    action_js: 'dynamicforms.defaultFilter(event);',
    action: null,
    label: 'Filter',
    title: 'Filter',
    icon: 'filter-outline',
    classes: null,
    displayStyle: {
      xs: {
        asButton: true,
        showLabel: true,
        showIcon: true,
      },
    },
  },
];

describe('actionsVuetify', () => {
  function mountComponent() {
    const test = mount(VuetifyActions, {
      propsData: {
        actions: _.cloneDeep(actionsCopy),
      },
      parentComponent: {
        name: 'DemoApp',
        data() {
          return { theme: 'vuetify' };
        },
      },
      stubs: {
        IonIcon: { template: '<div class="mocked-ionicon"/>' }
      },
      vuetify: new Vuetify(),
    });
    // Checks if buttons have been rendered
    return test.html();
  }

  it('checks if four buttons were rendered', async () => {
    const htmlCode = mountComponent();
    const buttonCounter = htmlCode.match(/<button /g).length;
    expect(buttonCounter)
      .toBe(4);
  });

  it('checks if add action is correctly rendered', async () => {
    const htmlCode = mountComponent();
    expect(htmlCode.match(/<span>\+ Add<\/span>/g))
      .not
      .toBeNull();
    expect(htmlCode.match(/<div class="mocked-ionicon action-icon" name="add-outline"><\/div>/g))
      .toBeNull();
  });

  it('checks if edit action is correctly rendered', async () => {
    const htmlCode = mountComponent();
    expect(htmlCode.match(/<span>Edit<\/span>/g))
      .not
      .toBeNull();
    expect(htmlCode.match(/<div class="mocked-ionicon action-icon" name="edit-outline"><\/div>/g))
      .not
      .toBeNull();
  });

  it('checks if delete action is correctly rendered', async () => {
    const htmlCode = mountComponent();
    expect(htmlCode.match(/<span>Delete<\/span>/g))
      .not
      .toBeNull();
    expect(htmlCode.match(/<div class="mocked-ionicon action-icon" name="trash-outline"><\/div>/g))
      .not
      .toBeNull();
  });

  it('checks if filter action is correctly rendered', async () => {
    const htmlCode = mountComponent();
    expect(htmlCode.match(/<span>Filter<\/span>/g))
      .not
      .toBeNull();
    expect(htmlCode.match(/<div class="mocked-ionicon action-icon" name="filter-outline"><\/div>/g))
      .not
      .toBeNull();
  });
});

describe('Check if visibility flags work as expected', () => {

  async function constructTest(asButton, showLabel, showIcon, clearLabelText) {
    const actions = _.cloneDeep(actionsCopy);
    if (clearLabelText === true) actions[0].label = null;
    actions[0].displayStyle = {
      xs: {
        asButton,
        showLabel,
        showIcon
      }
    };

    const test = mount(VuetifyActions, {
      propsData: { actions },
      stubs: { IonIcon: { template: '<div class="mocked-ionicon"/>' } },
    });
    await flushPromises();
    return test.html();
  }

  it('checks that - label and icon is shown in the button',
    async () => {
      const htmlCode = await constructTest(true, true, true);
      // preveriš, če se je v add knofu pokazala ikona IN labela
      const iconIsThere = (htmlCode.match(/<div class="mocked-ionicon action-icon" name="add-outline"><\/div>/g));
      const labelIsThere = (htmlCode.match(/<span>\+ Add<\/span>/g));
      expect(iconIsThere)
        .not
        .toBeNull();
      expect(labelIsThere)
        .not
        .toBeNull();
    });

  it('checks that - only icon is shown in the button (because label is not available)',
    async () => {
      const htmlCode = await constructTest(true, false, true);
      // preveriš, če se je v add knofu pokazala samo ikona
      const iconIsThere = (htmlCode.match(/<div class="mocked-ionicon action-icon" name="add-outline"><\/div>/g));
      expect(iconIsThere)
        .not
        .toBeNull();
    });

  it('checks that - only label is shown (because icon is not available)',
    async () => {
      const htmlCode = await constructTest(true, true, false);
      // preveriš, če se je v add knofu pokazala samo labela
      const labelIsThere = (htmlCode.match(/<span>\+ Add<\/span>/g));
      expect(labelIsThere)
        .not
        .toBeNull();
    });

  it('checks that - on delete label text - only icon is shown (because label is not available)',
    async () => {
      const htmlCode = await constructTest(true, true, true, true);
      const iconIsThere = htmlCode.match(/<div class="mocked-ionicon action-icon" name="add-outline"><\/div>/g);
      expect(iconIsThere)
        .not
        .toBeNull();
      expect(htmlCode.match(/<span>add<\/span>/g))
        .toBeNull();
    });

  it('checks that - on delete label text and hiding icon - only label from action name is shown (when no icon ' +
    'and no label, that\'s all that\'s left)',
    async () => {
      const htmlCode = await constructTest(true, true, false, true);
      const iconIsThere = htmlCode.match(/<div class="mocked-ionicon action-icon" name="add-outline"><\/div>/g);
      expect(iconIsThere)
        .toBeNull();
      expect(htmlCode.match(/<span>add<\/span>/g))
        .not
        .toBeNull();
    });
});

describe('Check if actions components are responsive', () => {
  function mountComponent() {
    const test = mount(VuetifyActions, {
      propsData: {
        actions: _.cloneDeep(actionsCopy)
          .splice(0),
      },
      parentComponent: {
        name: 'DemoApp',
        data() {
          return { theme: 'vuetify' };
        },
      },
      stubs: {
        IonIcon: { template: '<div class="mocked-ionicon"/>' }
      },
      vuetify: new Vuetify(),
    });
    // Checks if buttons have been rendered
    return test;
  }

  it('checks if xs breakpoint renders correctly', async () => {
    global.innerWidth = 500;
    const component = mountComponent();
    const htmlCode = component.html();
    const breakpoints = component.vm.$vuetify.breakpoint;
    expect(breakpoints.xs).toBe(true);
    expect(htmlCode.match(/<span>\+ Add<\/span>/g))
      .toBeNull();
    expect(htmlCode.match(/<div class="mocked-ionicon action-icon" name="add-outline"><\/div>/g))
      .not
      .toBeNull();
  });

  it('checks if md breakpoint renders correctly', async () => {
    global.innerWidth = 1024;
    const component = mountComponent();
    const htmlCode = component.html();
    const breakpoints = component.vm.$vuetify.breakpoint;
    expect(breakpoints.md).toBe(true);
    expect(htmlCode.match(/<span>\+ Add<\/span>/g))
      .not
      .toBeNull();
    expect(htmlCode.match(/<div class="mocked-ionicon action-icon" name="add-outline"><\/div>/g))
      .toBeNull();
  });

  it('checks if lg breakpoint renders correctly', async () => {
    global.innerWidth = 1300;
    const component = mountComponent();
    const htmlCode = component.html();
    const breakpoints = component.vm.$vuetify.breakpoint;
    expect(breakpoints.lg).toBe(true);
    expect(htmlCode.match(/<span>\+ Add<\/span>/g))
      .not
      .toBeNull();
    expect(htmlCode.match(/<div class="mocked-ionicon action-icon" name="add-outline"><\/div>/g))
      .not
      .toBeNull();
  });

  it('checks if xl breakpoint renders correctly', async () => {
    global.innerWidth = 2000;
    const component = mountComponent();
    const htmlCode = component.html();
    const breakpoints = component.vm.$vuetify.breakpoint;
    expect(breakpoints.xl).toBe(true);
    expect(htmlCode.match(/<span>\+ Add<\/span>/g))
      .not
      .toBeNull();
    expect(htmlCode.match(/<div class="mocked-ionicon action-icon" name="add-outline"><\/div>/g))
      .not
      .toBeNull();
  });
});