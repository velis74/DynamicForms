import { mount } from '@vue/test-utils';
import flushPromises from 'flush-promises';
import Vue from 'vue';
import Vuetify from 'vuetify';

import VuetifyActions from '../components/actions/actions_vuetify';
import * as VuetifyComponents from '../components/vuetify';

Vue.use(Vuetify);
Object.values(VuetifyComponents).map((component) => Vue.component(component.name, component));

describe('actionsVuetify', () => {
  it('check if elements are rendered', async () => {
    const test = mount(VuetifyActions, {
      propsData: {
        actions: [
          {
            position: 'FILTER_ROW_END',
            field_name: null,
            name: 'add',
            // eslint-disable-next-line max-len
            action_js: 'dynamicforms.newRow(\'{% url url_reverse|add:\'-detail\' pk=\'new\' format=\'html\' %}\', \'record\', __TABLEID__);',
            action: null,
            label: '+ Add',
            title: 'Add new record',
            icon: null,
            classes: null,
            displayStyle: {
              xs: {
                asButton: true,
                showLabel: false,
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
            icon: null,
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
            icon: null,
            classes: null,
            displayStyle: {
              xs: {
                asButton: true,
                showLabel: false,
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
            icon: null,
            classes: null,
            displayStyle: {
              xs: {
                asButton: true,
                showLabel: false,
                showIcon: true,
              },
            },
          },
        ],
      },
    });
    await flushPromises();
    // expect(test.html()).toContain('div');
    console.log(test.html());
  });
});
