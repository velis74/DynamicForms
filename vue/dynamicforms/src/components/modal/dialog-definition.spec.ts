import { VNode } from 'vue';

import DialogDefinition from './dialog-definition';
import { Dialogs } from './namespace';

test('DialogDefinition Constructor Test', () => {
  // Setup
  const title: string | VNode = 'Test Title';
  const body: Dialogs.DialogMessage = 'Test Body';
  const options: Dialogs.DialogOptions = { size: 5 };
  const actions = 'Test Actions';

  // Execution
  const dialog = new DialogDefinition(title, body, options, actions);

  // Assertion
  expect(dialog.title).toBe(title);
  expect(dialog.body).toBe(body);
  expect(dialog.options).toBe(options);
  expect(dialog.actions).toBe(actions);
  expect(dialog.dialogId).toBe(1);
});

test('DialogDefinition idGenerator Test', () => {
  // Setup
  const title: string | VNode = 'Test Title';
  const body: Dialogs.DialogMessage = 'Test Body';
  const options: Dialogs.DialogOptions = { size: 5 };
  const actions = 'Test Actions';

  // Execution
  const dialog1 = new DialogDefinition(title, body, options, actions);
  const dialog2 = new DialogDefinition(title, body, options, actions);

  // Assertion
  const dialogId1 = dialog1.dialogId;
  expect(dialog2.dialogId).toBe(dialogId1 + 1);
});

test('DialogDefinition topOfTheStack Test', () => {
  // Setup
  const title: string | VNode = 'Test Title';
  const body: Dialogs.DialogMessage = 'Test Body';
  const options: Dialogs.DialogOptions = { size: 5 };
  const actions = 'Test Actions';

  // Execution
  const dialog = new DialogDefinition(title, body, options, actions);

  // Assertion
  expect(dialog.topOfTheStack).toBe(false); // by default topOfTheStack should be false

  // Change topOfTheStack value
  dialog.topOfTheStack = true;

  // Assertion
  expect(dialog.topOfTheStack).toBe(true);
});
