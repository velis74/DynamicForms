import Action, { defaultActionHandler } from '../actions/action';
import FilteredActions from '../actions/filtered-actions';

import dfModal from './modal-view-api';

describe('Modal View API', () => {
  it('message generates correct dialog definition', async () => {
    const title = 'Test Title';
    const message = 'Test Message';
    const actions = new FilteredActions({ close: Action.closeAction({ actionClose: defaultActionHandler }) });

    const dialogPromise = dfModal.message(title, message, actions);

    const dialogDefinition = dfModal.getDialogDefinition(dialogPromise);
    const dialogById = dfModal.getDialogDefinition(dialogDefinition?.dialogId as number);

    // Trigger the action
    actions.actions.close.actionClose(
      actions.actions.close,
      undefined,
      { dialog: dialogDefinition },
    );
    const dialog = (await dialogPromise).dialog;

    expect(dialog.title).toEqual(title);
    expect(dialog.body).toEqual(message);
    expect(dialog.actions.actions.close).toBeDefined();

    expect(dialogById).toBe(dialog);
  });

  it('yesNo generates correct dialog definition', async () => {
    const title = 'Test Title';
    const question = 'Test Question';
    const actions = new FilteredActions({
      yes: Action.yesAction({ actionYes: defaultActionHandler }),
      no: Action.noAction({ actionNo: defaultActionHandler }),
    });

    const dialogPromise = dfModal.yesNo(title, question, actions);

    actions.actions.yes.actionYes(
      actions.actions.yes,
      undefined,
      { dialog: dfModal.getDialogDefinition(dialogPromise) },
    );
    const dialog = (await dialogPromise).dialog;

    expect(dialog.title).toEqual(title);
    expect(dialog.body).toEqual(question);
    expect(dialog.actions.actions.yes).toBeDefined();
    expect(dialog.actions.actions.no).toBeDefined();
    expect(dialog.actions.actions.close).not.toBeDefined();
  });
});
