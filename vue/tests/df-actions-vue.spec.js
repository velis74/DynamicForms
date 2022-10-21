import {mount, shallowMount} from "@vue/test-utils";
import Vue from 'vue';
import Vuetify from "vuetify";
import FilteredActions from "../components/actions/filtered-actions";

import Action from '../components/actions/action';
import DfActions from "../components/public/df-actions";
import VuetifyActions from "../components/actions/actions-vuetify";

Vue.use(Vuetify)

const fieldName = 'field-name';
const action_definitions = {
  // We have removed all properties non-essential for the FilteredActions class
  head: { position: 'HEADER', field_name: null, name: 'head' },
  rowStart: { position: 'ROW_START', field_name: null, name: 'rowStart' },
  rowEnd: { position: 'ROW_END', field_name: null, name: 'rowEnd' },
  rowClick: { position: 'ROW_CLICK', field_name: null, name: 'rowClick' },
  rowRightClick: { position: 'ROW_RIGHT_CLICK', field_name: null, name: 'rowRightClick' },
  fieldStart: { position: 'FIELD_START', field_name: fieldName, name: 'fieldStart' },
  fieldEnd: { position: 'FIELD_END', field_name: fieldName, name: 'fieldEnd' },
  formHeader: { position: "FORM_HEADER", field_name: null, name: 'formHeader'},
  formFooter: { position: "FORM_FOOTER", field_name: null, name: 'formFooter'},
}

const filtered_actions = new FilteredActions(action_definitions);

describe('df-actions', () => {
  it('check if dfactions renders vuetifyactions', async () => {
    expect(
      shallowMount(DfActions, {
        parentComponent: {
          name: 'DemoApp',
          data() {
            return { theme: 'vuetify' };
          },
        },
        stubs: {
          VuetifyActions: { template: '<div class="vuetifyactions"/>' }
        }
      }).html())
    .toContain('vuetifyactions')
  });
});

describe('vuetify-actions', () => {
  const get_actions = (type) => {
    return shallowMount(VuetifyActions, {
      parentComponent: {
        name: 'DemoApp',
        data() {
          return { theme: 'vuetify' };
        },
      },
    });
  };

  it('create empty vuetify actions', async () => {
    const action = get_actions();
    expect(action.exists()).toBe(true);
    const htmlCode = action.html();
    expect(htmlCode).not.toBeNull();

    expect(htmlCode).toStrictEqual('')
  });

  it('check whatever vuetify actions are generated', async () => {
    // create actions with filtered actions object
    const actions = get_actions();
    await actions.setProps({ actions: filtered_actions });
    // actions should be enveloped in the div
    expect(actions.html()).toContain('div');

    // create them with an array
    const actions1 = get_actions();
    await actions1.setProps({ actions: [Action.closeAction()] });
    // actions should be enveloped in the div
    expect(actions1.html()).toContain('div');
  });

  it('test each filtered action to be rendered', async () => {
    // header action
    const actions= get_actions();
    await actions.setProps({ actions: filtered_actions.header });
    expect(actions.html()).toContain(action_definitions.head.name);
    // row start action
    await actions.setProps({ actions: filtered_actions.rowStart });
    expect(actions.html()).toContain(action_definitions.rowStart.name);
    // row start action
    await actions.setProps({ actions: filtered_actions.rowEnd });
    expect(actions.html()).toContain(action_definitions.rowEnd.name);
    // row click action
    await actions.setProps({ actions: filtered_actions.rowClick });
    expect(actions.html()).toContain(action_definitions.rowClick.name);
    // row right click action
    await actions.setProps({ actions: filtered_actions.rowRightClick });
    expect(actions.html()).toContain(action_definitions.rowRightClick.name);
    // field start action
    await actions.setProps({ actions: filtered_actions.fieldStart(fieldName) });
    expect(actions.html()).toContain(action_definitions.fieldStart.name);
    // field end action
    await actions.setProps({ actions: filtered_actions.fieldEnd(fieldName) });
    expect(actions.html()).toContain(action_definitions.fieldEnd.name);
    // field all action
    await actions.setProps({ actions: filtered_actions.fieldAll(fieldName)});
    expect(actions.html()).toContain(action_definitions.fieldStart.name);
    expect(actions.html()).toContain(action_definitions.fieldEnd.name);
    // form header action
    await actions.setProps({ actions: filtered_actions.formHeader });
    expect(actions.html()).toContain(action_definitions.formHeader.name);
    // form footer action
    await actions.setProps({ actions: filtered_actions.formFooter });
    expect(actions.html()).toContain(action_definitions.formFooter.name);

    // render all
    await actions.setProps({ actions: filtered_actions });
    expect(actions.html()).toContain(action_definitions.head.name);
    expect(actions.html()).toContain(action_definitions.rowStart.name);
    expect(actions.html()).toContain(action_definitions.rowEnd.name);
    expect(actions.html()).toContain(action_definitions.rowClick.name);
    expect(actions.html()).toContain(action_definitions.rowRightClick.name);
    expect(actions.html()).toContain(action_definitions.fieldStart.name);
    expect(actions.html()).toContain(action_definitions.fieldEnd.name);
    expect(actions.html()).toContain(action_definitions.formHeader.name);
    expect(actions.html()).toContain(action_definitions.formFooter.name);
  });
});
