import FilteredActions from '../components/actions/filtered-actions';

describe('ButtonTesting', () => {
  it('Check if label / icon on button works', () => {
    const myActions = new FilteredActions({
      // We have removed all properties non-essential for the FilteredActions class
      head: { position: 'HEADER', field_name: null, name: 'head' },
      rstart: { position: 'ROW_START', field_name: null, name: 'rstart' },
      rend: { position: 'ROW_END', field_name: null, name: 'rend' },
      add: { position: 'FILTER_ROW_END', field_name: null, name: 'add' },
      description_help: { position: 'FIELD_START', field_name: 'description', name: 'description_help' },
      description_lookup: { position: 'FIELD_END', field_name: 'description', name: 'description_lookup' },
      datum_lookup: { position: 'FIELD_END', field_name: 'datum', name: 'datum_lookup' },
    });
    let fAct; // filtered actions. We use one variable for all sub-tests

    expect(myActions.actions).toBeDefined();
    expect(myActions.actions.add).toBeDefined();
    expect(myActions.actions.add.position).toBe('FILTER_ROW_END');

    expect(myActions.filterCache).toStrictEqual({});

    function simpleTest(actionsList, expectedCount, expectedNames, expectedCacheKey) {
      expect(actionsList.length).toEqual(expectedCount);
      for (let i = 0; i < expectedCount; i++) {
        expect(actionsList[i].name).toEqual(expectedNames[i]);
      }
      expect(myActions.filterCache[expectedCacheKey]).toBeDefined();
    }

    simpleTest(myActions.header, 1, ['head'], 'HEADER');
    simpleTest(myActions.rowStart, 1, ['rstart'], 'ROW_START');
    simpleTest(myActions.rowEnd, 1, ['rend'], 'ROW_END');
    simpleTest(myActions.fieldStart('description'), 1, ['description_help'], 'FIELD_START|description');
    simpleTest(myActions.fieldEnd('description'), 1, ['description_lookup'], 'FIELD_END|description');
    simpleTest(myActions.fieldEnd('datum'), 1, ['datum_lookup'], 'FIELD_END|datum');

    fAct = myActions.fieldAll('description').list;
    simpleTest(fAct, 2, ['description_help', 'description_lookup'], 'FIELD_START|description');
    expect(myActions.filterCache['FIELD_END|description']).toBeDefined();

    fAct = myActions.fieldEnd('field_without_actions');
    simpleTest(fAct, 0, [], 'FIELD_END|field_without_actions');
    expect(fAct[0]).toBeUndefined();
    expect(myActions.filterCache['FIELD_END|field_without_actions'].list.length).toEqual(0);
  });
});
