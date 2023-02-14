import _ from 'lodash';

import Action from '../../components/actions/action';
import FilteredActions from '../../components/actions/filtered-actions';

describe('Actions', () => {
  it('Basic instance creation tests', () => {
    const myActions = new FilteredActions({
      // We have removed all properties non-essential for the FilteredActions class
      head: { position: 'HEADER', name: 'head' },
      rstart: { position: 'ROW_START', name: 'rstart' },
      rend: { position: 'ROW_END', name: 'rend' },
      add: { position: 'ROW_END', name: 'add' },
      description_help: { position: 'FIELD_START', field_name: 'description', name: 'description_help' },
      description_lookup: { position: 'FIELD_END', field_name: 'description', name: 'description_lookup' },
      datum_lookup: { position: 'FIELD_END', field_name: 'datum', name: 'datum_lookup' },
    });
    let fAct; // filtered actions. We use one variable for all sub-tests

    expect(myActions.actions).toBeDefined();
    expect(myActions.actions.add).toBeDefined();
    expect(myActions.actions.add.position).toBe('ROW_END');

    expect(myActions.filterCache).toStrictEqual({});

    function simpleTest(actions: FilteredActions, expectedNames: string[], expectedCacheKey: string) {
      expect(actions.length).toEqual(expectedNames.length);
      for (const action: Action of _.zip(actions.actionsList, expectedNames)) {
        expect(action[0].name).toEqual(action[1]);
      }
      expect(myActions.filterCache[expectedCacheKey]).toBeDefined();
    }

    simpleTest(myActions.header, ['head'], 'HEADER');
    simpleTest(myActions.rowStart, ['rstart'], 'ROW_START');
    simpleTest(myActions.rowEnd, ['rend'], 'ROW_END');
    simpleTest(myActions.fieldStart('description'), ['description_help'], 'FIELD_START|description');
    simpleTest(myActions.fieldEnd('description'), ['description_lookup'], 'FIELD_END|description');
    simpleTest(myActions.fieldEnd('datum'), ['datum_lookup'], 'FIELD_END|datum');

    fAct = myActions.fieldAll('description');
    simpleTest(fAct, ['description_help', 'description_lookup'], 'FIELD_START|description');
    expect(myActions.filterCache['FIELD_END|description']).toBeDefined();

    fAct = myActions.fieldEnd('field_without_actions');
    simpleTest(fAct, [], 'FIELD_END|field_without_actions');
    expect(fAct[0]).toBeUndefined();
    expect(myActions.filterCache['FIELD_END|field_without_actions'].length).toEqual(0);
  });
});
