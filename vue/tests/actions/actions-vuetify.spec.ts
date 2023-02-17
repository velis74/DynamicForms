import { mount } from '@vue/test-utils';
import { createVuetify } from 'vuetify';

import Action, { defaultActionHandler } from '../../components/actions/action';
import VuetifyActions from '../../components/actions/actions-vuetify.vue';
import FilteredActions from '../../components/actions/filtered-actions';

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

describe('vuetify-actions', () => {
  function getActions() {
    return mount(
      VuetifyActions,
      {
        propsData: { actions: new FilteredActions([]) },
        global: { plugins: [vuetify] },
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
