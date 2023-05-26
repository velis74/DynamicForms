import FilteredActions from '../actions/filtered-actions';

import dialogList, { DialogDefinition } from './modal-view-list';

describe('DialogList', () => {
  // eslint-disable-next-line no-undef
  it('Check if empty list returns null as current dialog', () => {
    expect(dialogList).toBeDefined();
    expect(dialogList.current).toEqual(null);
  });
  it('Check if non-empty list returns a proper DialogDefinition object and promise is good', () => {
    const dialogDef = new DialogDefinition('aha', null, null, null);
    const dialogId = dialogList.push(dialogDef);
    expect(dialogList.current).not.toBeNull();
    expect(dialogList.current?.dialogId).toEqual(dialogId);
    expect(dialogList.current?.title).toEqual('aha');

    // Check if we can retrieve dialog definition from the ID the API had given us
    expect(dialogList.getDialogFromId(dialogId)).toEqual(dialogDef);
    // We request for a dialog with an id that doesn't exist
    expect(dialogList.getDialogFromId(dialogId + 1)).toBeNull();

    const promise = dialogDef?.promise;
    expect(dialogList.isCurrentDialogPromise(promise)).toBeTruthy();
    expect(dialogList.getDialogDefFromPromise(promise)).toEqual(dialogDef);
  });
  it('Check if updating existing dialog really updates it', () => {
    dialogList.push(new DialogDefinition('test', null, null, null), 1);
    expect(dialogList.current).toBeDefined();
    expect(dialogList.current?.dialogId).toEqual(1);
    expect(dialogList.current?.title).toEqual('test');
    expect(dialogList.current?.topOfTheStack).toEqual(true);
  });
  it('Check if adding another dialog properly updates the topOfTheStack member', () => {
    dialogList.push(new DialogDefinition('second', null, null, null));
    expect(dialogList.current).toBeDefined();
    expect(dialogList.current?.topOfTheStack).toEqual(true);
    expect(dialogList.list?.length).toEqual(2);
    expect(dialogList.list[0]?.topOfTheStack).toEqual(false);
  });
  it('Check if popping the second dialog properly updates the topOfTheStack member of the first one', () => {
    dialogList.pop(3);
    expect(dialogList.current).toBeDefined();
    expect(dialogList.current?.topOfTheStack).toEqual(true);
    expect(dialogList.list?.length).toEqual(1);
  });
  it('Check if popping the only dialog produces an empty list again', () => {
    dialogList.pop(1);
    expect(dialogList.current).toEqual(null);
  });
  it('Check if adding a dialog with FilteredActions modifies the actions payload', () => {
    const actions = new FilteredActions({ testAction: { position: 'HEADER', name: 'testAction' } });
    const dialogDef = new DialogDefinition('test', null, { size: 5 }, actions);

    dialogList.push(dialogDef);

    expect(dialogList.current).toBeDefined();
    expect(dialogList.current?.actions.payload).toBeDefined();
    expect(dialogList.current?.actions.payload['$extra-data'].dialog).toEqual(dialogDef);
  });
});
