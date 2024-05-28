import { flushPromises, mount } from '@vue/test-utils';
import _ from 'lodash';
import { vi } from 'vitest';
import { nextTick } from 'vue';
import { createVuetify } from 'vuetify';

import * as VuetifyComponents from '../vuetify';

import Action, { defaultActionHandler } from './action';
import VuetifyActions from './actions-vuetify.vue';
import FilteredActions from './filtered-actions';

const fieldName = 'field-name';
const actionDefinitions = {
  // We have removed all properties non-essential for the FilteredActions class
  head: { position: 'HEADER', name: 'head' },
  rowStart: { position: 'ROW_START', name: 'rowStart' },
  rowEnd: { position: 'ROW_END', name: 'rowEnd' },
  rowClick: { position: 'ROW_CLICK', name: 'rowClick' },
  rowRightClick: { position: 'ROW_RIGHT_CLICK', name: 'rowRightClick' },
  fieldStart: { position: 'FIELD_START', field_name: fieldName, name: 'fieldStart' },
  fieldEnd: { position: 'FIELD_END', field_name: fieldName, name: 'fieldEnd' },
  formHeader: { position: 'FORM_HEADER', name: 'formHeader' },
  formFooter: { position: 'FORM_FOOTER', name: 'formFooter' },
};

const filteredActions = new FilteredActions(actionDefinitions);
const vuetify = createVuetify();

async function setViewPortSize(newWidth: number, newHeight?: number) {
  const window = document.defaultView;

  expect(window).not.toBeNull();
  if (window == null) return;

  // Set the viewport width and height
  // noinspection JSConstantReassignment
  window.innerWidth = newWidth || 1024;
  // noinspection JSConstantReassignment
  window.innerHeight = newHeight || 1024;

  // Create and dispatch a new resize event
  const event = new UIEvent('resize');
  window.dispatchEvent(event);

  // Assert that the viewport width and height have changed
  expect(window.innerWidth).toBe(newWidth || 1024);
  expect(window.innerHeight).toBe(newHeight || 1024);

  await nextTick();
}

describe('vuetify-actions', () => {
  function getActions() {
    return mount(
      VuetifyActions,
      {
        propsData: { actions: new FilteredActions([]) },
        global: { plugins: [vuetify], components: VuetifyComponents, provide: { $df$ApplicationTheme: 'vuetify' } },
      },
    );
  }

  it('create empty vuetify actions', async () => {
    const action = getActions();
    expect(action.exists()).toBe(true);
    const htmlCode = action.html();
    expect(htmlCode).not.toBeNull();

    expect(htmlCode).toStrictEqual('<!--v-if-->');
  });

  it('check whatever vuetify actions are generated', async () => {
    // create actions with filtered actions object
    const actions = getActions();
    await actions.setProps({ actions: filteredActions });
    // actions should be enveloped in the div
    expect(actions.html()).toContain('div');

    // create them with an array
    const actions1 = getActions();
    await actions1.setProps(
      { actions: new FilteredActions([Action.closeAction({ actionClose: defaultActionHandler })]) },
    );
    // actions should be enveloped in the div
    expect(actions1.html()).toContain('div');
  });

  it('test each filtered action to be rendered', async () => {
    // header action
    const actions = getActions();
    await actions.setProps({ actions: new FilteredActions({ head: filteredActions.actions.head }) });
    expect(actions.html()).toContain(actionDefinitions.head.name);

    // row start action
    await actions.setProps({ actions: filteredActions.rowStart });
    expect(actions.html()).toContain(actionDefinitions.rowStart.name);
    // row start action
    await actions.setProps({ actions: filteredActions.rowEnd });
    expect(actions.html()).toContain(actionDefinitions.rowEnd.name);
    // row click action
    await actions.setProps({ actions: filteredActions.rowClick });
    expect(actions.html()).toContain(actionDefinitions.rowClick.name);
    // row right click action
    await actions.setProps({ actions: filteredActions.rowRightClick });
    expect(actions.html()).toContain(actionDefinitions.rowRightClick.name);
    // field start action
    await actions.setProps({ actions: filteredActions.fieldStart(fieldName) });
    expect(actions.html()).toContain(actionDefinitions.fieldStart.name);
    // field end action
    await actions.setProps({ actions: filteredActions.fieldEnd(fieldName) });
    expect(actions.html()).toContain(actionDefinitions.fieldEnd.name);
    // field all action
    await actions.setProps({ actions: filteredActions.fieldAll(fieldName) });
    expect(actions.html()).toContain(actionDefinitions.fieldStart.name);
    expect(actions.html()).toContain(actionDefinitions.fieldEnd.name);
    // form header action
    await actions.setProps({ actions: filteredActions.formHeader });
    expect(actions.html()).toContain(actionDefinitions.formHeader.name);
    // form footer action
    await actions.setProps({ actions: filteredActions.formFooter });
    expect(actions.html()).toContain(actionDefinitions.formFooter.name);

    // render all
    await actions.setProps({ actions: filteredActions });
    expect(actions.html()).toContain(actionDefinitions.head.name);
    expect(actions.html()).toContain(actionDefinitions.rowStart.name);
    expect(actions.html()).toContain(actionDefinitions.rowEnd.name);
    expect(actions.html()).toContain(actionDefinitions.rowClick.name);
    expect(actions.html()).toContain(actionDefinitions.rowRightClick.name);
    expect(actions.html()).toContain(actionDefinitions.fieldStart.name);
    expect(actions.html()).toContain(actionDefinitions.fieldEnd.name);
    expect(actions.html()).toContain(actionDefinitions.formHeader.name);
    expect(actions.html()).toContain(actionDefinitions.formFooter.name);
  });
});

vi.mock('axios', () => ({
  default: {
    create: () => ({
      interceptors: {
        request: {
          use: () => {
          },
        },
        response: {
          use: () => {
          },
        },
      },
    }),
    get: async (url) => {
      if (url.includes('failure')) throw new Error('bad url');
      return {
        data: '<svg xmlns="http://www.w3.org/2000/svg" class="ionicon" ' +
          'viewBox="0 0 512 512"><title>Warning</title><path d="M449.07 399.08L278.64 82.58c-12.08-22.44-44.26-22.44' +
          '-56.35 0L51.87 399.08A32 32 0 0080 446.25h340.89a32 32 0 0028.18-47.17zm-198.6-1.83a20 20 0 1120-20 20 20' +
          ' 0 01-20 20zm21.72-201.15l-5.74 122a16 16 0 01-32 0l-5.74-121.95a21.73 21.73 0 0121.5-22.69h.21a21.74' +
          ' 21.74 0 0121.73 22.7z"/></svg>',
      };
    },
  },
}));

const actionsCopy = {
  add: {
    position: 'ROW_END',
    field_name: null,
    name: 'add',
    // eslint-disable-next-line max-len
    action: null,
    label: 'Add',
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
  edit: {
    position: 'ROW_CLICK',
    field_name: null,
    name: 'edit',
    // eslint-disable-next-line max-len
    action: null,
    label: 'Edit',
    title: 'Edit record',
    icon: 'edit-outline',
    classes: null,
    displayStyle: null,
  },
  delete: {
    position: 'ROW_END',
    field_name: null,
    name: 'delete',
    // eslint-disable-next-line max-len
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
  filter: {
    position: 'ROW_END',
    field_name: null,
    name: 'filter',
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
};

describe('vuetify-actions action rendering', () => {
  function mountComponent() {
    return mount(VuetifyActions, {
      propsData: { actions: new FilteredActions(actionsCopy) },
      global: {
        plugins: [vuetify],
        components: VuetifyComponents,
        provide: { $df$ApplicationTheme: 'vuetify' },
        stubs: { IonIcon: { template: '<div class="mocked-ionicon"/>' } },
      },
    }).html();
  }

  it('checks if four buttons were rendered', async () => {
    const htmlCode = mountComponent();
    const buttonCounter = htmlCode.match(/<button /g)?.length;
    expect(buttonCounter).toBe(4);
  });

  it('checks if add action is correctly rendered', async () => {
    await setViewPortSize(1024); // ensure md or up so that the label is drawn
    const htmlCode = mountComponent();
    expect(htmlCode.match(/<span(\sdata-v-\w+="")?>Add<\/span>/g)).not.toBeNull();
    expect(htmlCode.match(/<div class="mocked-ionicon action-icon" name="add-outline"><\/div>/g)).toBeNull();
  });

  it('checks if edit action is correctly rendered', async () => {
    const htmlCode = mountComponent();
    expect(htmlCode.match(/<span(\sdata-v-\w+="")?>Edit<\/span>/g)).not.toBeNull();
    expect(htmlCode.match(/<div(\sdata-v-\w+="")? class="mocked-ionicon action-icon" name="edit-outline"><\/div>/g))
      .not.toBeNull();
  });

  it('checks if delete action is correctly rendered', async () => {
    const htmlCode = mountComponent();
    expect(htmlCode.match(/<span(\sdata-v-\w+="")?>Delete<\/span>/g)).not.toBeNull();
    expect(htmlCode.match(/<div(\sdata-v-\w+="")? class="mocked-ionicon action-icon" name="trash-outline"><\/div>/g))
      .not.toBeNull();
  });

  it('checks if filter action is correctly rendered', async () => {
    const htmlCode = mountComponent();
    expect(htmlCode.match(/<span(\sdata-v-\w+="")?>Filter<\/span>/g)).not.toBeNull();
    expect(htmlCode.match(/<div(\sdata-v-\w+="")? class="mocked-ionicon action-icon" name="filter-outline"><\/div>/g))
      .not.toBeNull();
  });
});

describe('Check if visibility flags work as expected', () => {
  async function constructTest(asButton, showLabel, showIcon, clearLabelText) {
    const actions = _.cloneDeep(actionsCopy);
    if (clearLabelText === true) actions.add.label = null;
    actions.add.displayStyle = {
      xs: {
        asButton,
        showLabel,
        showIcon,
      },
    };

    const test = mount(VuetifyActions, {
      propsData: { actions: new FilteredActions(actions) },
      global: {
        plugins: [vuetify],
        components: VuetifyComponents,
        provide: { $df$ApplicationTheme: 'vuetify' },
        stubs: { IonIcon: { template: '<div class="mocked-ionicon"/>' } },
      },
    });
    await flushPromises();
    return test.html();
  }

  it(
    'checks that - label and icon is shown in the button',
    async () => {
      const htmlCode = await constructTest(true, true, true);
      // preveriš, če se je v add knofu pokazala ikona IN labela
      const iconIsThere = (htmlCode.match(
        /<div(\sdata-v-\w+="")? class="mocked-ionicon action-icon" name="add-outline"><\/div>/g,
      ));
      const labelIsThere = (htmlCode.match(/<span(\sdata-v-\w+="")?>Add<\/span>/g));
      expect(iconIsThere).not.toBeNull();
      expect(labelIsThere).not.toBeNull();
    },
  );

  it(
    'checks that - only icon is shown in the button (because label is not available)',
    async () => {
      const htmlCode = await constructTest(true, false, true);
      // preveriš, če se je v add knofu pokazala samo ikona
      const iconIsThere = (htmlCode.match(
        /<div(\sdata-v-\w+="")? class="mocked-ionicon action-icon" name="add-outline"><\/div>/g,
      ));
      expect(iconIsThere).not.toBeNull();
    },
  );

  it(
    'checks that - only label is shown (because icon is not available)',
    async () => {
      const htmlCode = await constructTest(true, true, false);
      // preveriš, če se je v add knofu pokazala samo labela
      const labelIsThere = (htmlCode.match(/<span(\sdata-v-\w+="")?>Add<\/span>/g));
      expect(labelIsThere).not.toBeNull();
    },
  );

  it(
    'checks that - on delete label text - only icon is shown (because label is not available)',
    async () => {
      const htmlCode = await constructTest(true, true, true, true);
      const iconIsThere = htmlCode.match(
        /<div(\sdata-v-\w+="")? class="mocked-ionicon action-icon" name="add-outline"><\/div>/g,
      );
      expect(iconIsThere).not.toBeNull();
      expect(htmlCode.match(/<span(\sdata-v-\w+="")?>add<\/span>/g)).toBeNull();
    },
  );

  it(
    'checks that - on delete label text and hiding icon - only label from action name is shown (when no icon ' +
    'and no label, that\'s all that\'s left)',
    async () => {
      const htmlCode = await constructTest(true, true, false, true);
      const iconIsThere = htmlCode.match(
        /<div(\sdata-v-\w+="")? class="mocked-ionicon action-icon" name="add-outline"><\/div>/g,
      );
      expect(iconIsThere).toBeNull();
      expect(htmlCode.match(/<span(\sdata-v-\w+="")?>add<\/span>/g)).not.toBeNull();
    },
  );
});

describe('Check if actions components are responsive', () => {
  function mountComponent() {
    return mount(VuetifyActions, {
      propsData: { actions: new FilteredActions([actionsCopy.add]) },
      global: {
        plugins: [vuetify],
        components: VuetifyComponents,
        provide: { $df$ApplicationTheme: 'vuetify' },
        stubs: { IonIcon: { template: '<div class="mocked-ionicon"/>' } },
      },
    });
  }

  it('checks if xs breakpoint renders correctly', async () => {
    await setViewPortSize(500);

    const component = mountComponent();
    const htmlCode = component.html();
    const breakpoints = component.vm.$vuetify.display;
    expect(breakpoints.xs).toBe(true);
    expect(htmlCode.match(/<span(\sdata-v-\w+="")?>Add<\/span>/g)).toBeNull();
    expect(htmlCode.match(/<div(\sdata-v-\w+="")? class="mocked-ionicon action-icon" name="add-outline"><\/div>/g))
      .not.toBeNull();
  });

  it('checks if md breakpoint renders correctly', async () => {
    await setViewPortSize(1024);
    const component = mountComponent();
    const htmlCode = component.html();
    const breakpoints = component.vm.$vuetify.display;
    expect(breakpoints.md).toBe(true);
    expect(htmlCode.match(/<span(\sdata-v-\w+="")?>Add<\/span>/g)).not.toBeNull();
    expect(htmlCode.match(/<div(\sdata-v-\w+="")? class="mocked-ionicon action-icon" name="add-outline"><\/div>/g))
      .toBeNull();
  });

  it('checks if lg breakpoint renders correctly', async () => {
    await setViewPortSize(1300);
    const component = mountComponent();
    const htmlCode = component.html();
    const breakpoints = component.vm.$vuetify.display;
    expect(breakpoints.lg).toBe(true);
    expect(htmlCode.match(/<span(\sdata-v-\w+="")?>Add<\/span>/g)).not.toBeNull();
    expect(htmlCode.match(/<div(\sdata-v-\w+="")? class="mocked-ionicon action-icon" name="add-outline"><\/div>/g))
      .not.toBeNull();
  });

  it('checks if xl breakpoint renders correctly', async () => {
    await setViewPortSize(2000);
    const component = mountComponent();
    const htmlCode = component.html();
    const breakpoints = component.vm.$vuetify.display;
    expect(breakpoints.xl).toBe(true);
    expect(htmlCode.match(/<span(\sdata-v-\w+="")?>Add<\/span>/g)).not.toBeNull();
    expect(htmlCode.match(/<div(\sdata-v-\w+="")? class="mocked-ionicon action-icon" name="add-outline"><\/div>/g))
      .not.toBeNull();
  });
});
