import { vi } from 'vitest';

import FormPayload from '../form/definitions/form-payload';

import Action, { defaultActionHandler } from './action';

describe('Action', () => {
  describe('defaultActionHandler', () => {
    const payload = FormPayload.create();
    const action = new Action({ name: 'test-action', position: 'HEADER', fieldName: 'test-field' });

    it('resolves the dialog promise and closes it when it is present in extraData', () => {
      const extraData = { dialog: { resolvePromise: vi.fn(), close: vi.fn() } };
      defaultActionHandler(action, payload, extraData);

      expect(extraData.dialog.resolvePromise).toHaveBeenCalledWith({
        action,
        payload,
        extraData,
        dialog: extraData.dialog,
      });
      expect(extraData.dialog.close).toHaveBeenCalled();
    });

    it('defaultActionHandler returns true', () => {
      const extraData = { dialog: { resolvePromise: vi.fn(), close: vi.fn() } };
      const result = defaultActionHandler(action, payload, extraData);

      expect(result).toBe(true);
    });

    it('does not call resolvePromise or close when dialog is not present in extraData', () => {
      const extraData = { dialog: { resolvePromise: vi.fn(), close: vi.fn() } };
      const noDialogExtraData = <any>{};
      defaultActionHandler(action, payload, noDialogExtraData);

      expect(extraData.dialog.resolvePromise).not.toHaveBeenCalled();
      expect(extraData.dialog.close).not.toHaveBeenCalled();
    });
  });

  describe('Action class', () => {
    it('creates an action with the expected properties', () => {
      const actionData = {
        name: 'test-action',
        position: 'HEADER',
        field_name: 'test-field',
        label: 'Test action',
        labelAvailable: true,
        icon: 'test-icon',
        iconAvailable: true,
        displayStyle: {
          xl: { showLabel: true, showIcon: true, asButton: false },
          sm: { showLabel: false, showIcon: false, asButton: true },
        },
        payload: FormPayload.create(),
      };
      const action = new Action(actionData);

      expect(action).toHaveProperty('name', 'test-action');
      expect(action).toHaveProperty('uniqueId');
      expect(action).toHaveProperty('position', 'HEADER');
      expect(action).toHaveProperty('fieldName', 'test-field');
      expect(action).toHaveProperty('label', 'Test action');
      expect(action).toHaveProperty('labelAvailable', true);
      expect(action).toHaveProperty('icon', 'test-icon');
      expect(action).toHaveProperty('iconAvailable', true);
      expect(action).toHaveProperty('displayStyle', {
        xl: { showLabel: true, showIcon: true, asButton: false },
        sm: { showLabel: false, showIcon: false, asButton: true },
      });
      expect(action).toHaveProperty('payload');
    });
    it('throws an error if the name does not match the pattern', () => {
      const consoleWarnSpy = vi.spyOn(console, 'warn').mockImplementation(() => { });
      const actionData = {
        name: 'Invalid Name',
        position: 'HEADER',
      };
      new Action(actionData); // eslint-disable-line no-new
      expect(consoleWarnSpy).toHaveBeenCalledWith(
        'Action name must be a valid string, matching [a-zA-Z-_]+. Got Invalid Name.' +
        ' Impossible to construct handler function name',
        actionData,
      );

      consoleWarnSpy.mockRestore();
    });
    it('warns that an unknown action position is specified', () => {
      const consoleWarnSpy = vi.spyOn(console, 'warn').mockImplementation(() => { });
      const actionData = {
        name: 'add',
        position: 'HEADER_INVALID',
      };
      new Action(actionData); // eslint-disable-line no-new
      expect(consoleWarnSpy).toHaveBeenCalledWith('Action position HEADER_INVALID not known', actionData);

      consoleWarnSpy.mockRestore();
    });

    it('does not throw an error if the name matches the pattern', () => {
      const consoleWarnSpy = vi.spyOn(console, 'warn').mockImplementation(() => { });
      const actionData = {
        name: 'valid-name',
        position: 'HEADER',
      };
      new Action(actionData); // eslint-disable-line no-new
      expect(consoleWarnSpy).not.toHaveBeenCalled();

      consoleWarnSpy.mockRestore();
    });

    it('gets fieldName from JSON', () => {
      const action1 = new Action({ name: 'test', position: 'HEADER', field_name: 'field1' });
      expect(action1.fieldName).toEqual('field1');
      const action2 = new Action({ name: 'test', position: 'HEADER', fieldName: 'field1' });
      expect(action2.fieldName).toBeNull();
    });

    it('gets fieldName from Action object', () => {
      const action1 = new Action({ name: 'test', position: 'HEADER', field_name: 'field1' });
      expect(action1.fieldName).toEqual('field1');
      const action2 = new Action(action1);
      expect(action2.fieldName).toEqual('field1');
    });
  });

  describe('Action template functions', () => {
    it('actionClose() should return an Action object with correct values', () => {
      const action = Action.closeAction();
      expect(action).toBeInstanceOf(Action);
      expect(action).toHaveProperty('name', 'close');
      expect(action).toHaveProperty('uniqueId');
      expect(action.uniqueId).toEqual(expect.any(Number));
      expect(action).toHaveProperty('position', 'FORM_FOOTER');
      expect(action).toHaveProperty('label', 'Close');
      expect(action).toHaveProperty('labelAvailable', true);
      expect(action).toHaveProperty('icon', 'ion-close-outline');
      expect(action).toHaveProperty('iconAvailable', true);
    });

    it('actionYes() should return an Action object with correct values', () => {
      const action = Action.yesAction();
      expect(action).toBeInstanceOf(Action);
      expect(action).toHaveProperty('name', 'yes');
      expect(action).toHaveProperty('uniqueId');
      expect(action.uniqueId).toEqual(expect.any(Number));
      expect(action).toHaveProperty('position', 'FORM_FOOTER');
      expect(action).toHaveProperty('label', 'Yes');
      expect(action).toHaveProperty('labelAvailable', true);
      expect(action).toHaveProperty('icon', 'ion-thumbs-up-outline');
      expect(action).toHaveProperty('iconAvailable', true);
    });

    it('actionNo() should return an Action object with correct values', () => {
      const action = Action.noAction();
      expect(action).toBeInstanceOf(Action);
      expect(action).toHaveProperty('name', 'no');
      expect(action).toHaveProperty('uniqueId');
      expect(action.uniqueId).toEqual(expect.any(Number));
      expect(action).toHaveProperty('position', 'FORM_FOOTER');
      expect(action).toHaveProperty('label', 'No');
      expect(action).toHaveProperty('labelAvailable', true);
      expect(action).toHaveProperty('icon', 'ion-thumbs-down-outline');
      expect(action).toHaveProperty('iconAvailable', true);
    });
  });
});
