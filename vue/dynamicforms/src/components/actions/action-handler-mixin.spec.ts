import { mount, VueWrapper } from '@vue/test-utils';
import { vi } from 'vitest';
import { createVuetify } from 'vuetify';

import FormPayload from '../form/definitions/form-payload';

import ActionHandlerMixin from './action-handler-mixin';
import FilteredActions from './filtered-actions';

const actions = {
  head: { position: 'HEADER', name: 'head' },
  rstart: { position: 'ROW_START', name: 'rstart' },
  rend: { position: 'ROW_END', name: 'rend' },
  add: { position: 'ROW_END', name: 'add' },
  description_help: { position: 'FIELD_START', field_name: 'description', name: 'description_help' },
  description_lookup: { position: 'FIELD_END', field_name: 'description', name: 'description_lookup' },
  datum_lookup: {
    position: 'FIELD_END',
    field_name: 'datum',
    name: 'datum_lookup',
    actionDatumLookup() { return false; },
  },
};

describe('ActionHandlerMixin with default action processor', () => {
  const vuetify = createVuetify();
  let wrapper: VueWrapper<any>;

  const component = {
    template: '<div></div>',
    mixins: [ActionHandlerMixin],
    methods: {
      async actionDefaultProcessor() {
        return true;
      },
      async actionHead() {
        return true;
      },
    },
  };

  beforeEach(() => {
    wrapper = mount(component, {
      global: {
        stubs: ['DfForm', 'DfTable', 'DfFormLayout'],
        plugins: [vuetify],
      },
    });
  });

  afterEach(() => {
    wrapper.unmount();
  });

  it('dispatches an action and calls a handler function', async () => {
    const dispatchActionSpy = vi.spyOn(wrapper.vm, 'dispatchAction');
    const actionDefaultProcessorSpy = vi.spyOn(wrapper.vm, 'actionDefaultProcessor');
    const actionHeadSpy = vi.spyOn(wrapper.vm, 'actionHead');
    const testActions = new FilteredActions({ head: actions.head, rstart: actions.rstart });

    await wrapper.vm.dispatchAction(testActions);
    expect(dispatchActionSpy).toHaveBeenCalledTimes(1);
    expect(dispatchActionSpy).toHaveBeenNthCalledWith(1, testActions);
    // expect(dispatchActionSpy).toHaveBeenNthCalledWith(2, testActions.actions.head, undefined);
    // expect(dispatchActionSpy).toHaveBeenNthCalledWith(3, testActions.actions.rstart, undefined);
    expect(actionHeadSpy).toHaveBeenCalledWith(testActions.actions.head, undefined, {});
    expect(actionDefaultProcessorSpy).toHaveBeenCalledWith(testActions.actions.rstart, undefined, {});
  });

  it('dispatches action with payload', async () => {
    const payload = new FormPayload({ description: 'my test description' });
    const actionsWithPayload = new FilteredActions(actions, payload);
    const actionDefaultProcessorSpy = vi.spyOn(wrapper.vm, 'actionDefaultProcessor');

    await wrapper.vm.dispatchAction(actionsWithPayload.actions.description_help, {});
    expect(actionDefaultProcessorSpy).toHaveBeenCalledWith(actionsWithPayload.actions.description_help, payload, {});
    expect(wrapper.emitted()['action-executed']).toBeTruthy();
  });

  it('dispatches action without payload', async () => {
    const payload = null;
    const actionsWithPayload = new FilteredActions(actions, payload);
    const actionDefaultProcessorSpy = vi.spyOn(wrapper.vm, 'actionDefaultProcessor');

    await wrapper.vm.dispatchAction(actionsWithPayload.actions.description_help, {});
    expect(actionDefaultProcessorSpy).toHaveBeenCalledWith(actionsWithPayload.actions.description_help, payload, {});
    expect(wrapper.emitted()['action-executed']).toBeTruthy();
  });

  /*
  it('handles filtered actions', async () => {
    const action1 = { name: 'test-action-1', payload: { foo: 'bar' } };
    const action2 = { name: 'test-action-2', payload: { foo: 'baz' } };
    const handlerFn1 = jest.fn().mockReturnValue(true);
    const handlerFn2 = jest.fn().mockReturnValue(true);
    wrapper.setMethods({
      getHandlersWithPayload: jest.fn().mockReturnValue([{
        instance: { actionTestAction1: handlerFn1 }, methodName: 'actionTestAction1', payload: action1.payload
      }]),
    });
    await wrapper.vm.dispatchAction([action1, action2], {});
    expect(handlerFn1).toHaveBeenCalled();
    expect(wrapper.emitted()['action-executed']).toBeTruthy();
  });

  */
  it('handles action with a specific handler', async () => {
    const payload = null;
    const actionsWithNoPayload = new FilteredActions(actions, payload);
    const actionDatumLookupSpy = vi.spyOn(actionsWithNoPayload.actions.datum_lookup, 'actionDatumLookup');

    const datumLookupAction = actionsWithNoPayload.actions.datum_lookup;
    await wrapper.vm.dispatchAction(datumLookupAction, {});
    expect(actionDatumLookupSpy).toHaveBeenCalledWith(datumLookupAction, payload, {});
    expect(wrapper.emitted()['action-executed'])
      .toEqual([[{ action: datumLookupAction, payload: null, ed: {}, actionHandled: true }]]);
  });
});

describe('ActionHandlerMixin without default action processor', () => {
  const vuetify = createVuetify();
  let wrapper: VueWrapper<any>;

  const component = {
    template: '<div></div>',
    mixins: [ActionHandlerMixin],
    methods: {
      async actionHead() {
        return true;
      },
    },
  };

  beforeEach(() => {
    wrapper = mount(component, {
      global: {
        stubs: ['DfForm', 'DfTable', 'DfFormLayout'],
        plugins: [vuetify],
      },
    });
  });

  afterEach(() => {
    wrapper.unmount();
  });

  it('dispatches an action that has no handler', async () => {
    const dispatchActionSpy = vi.spyOn(wrapper.vm, 'dispatchAction');
    const testActions = new FilteredActions({ head: actions.head, rstart: actions.rstart });

    await wrapper.vm.dispatchAction(testActions.actions.rstart);
    expect(dispatchActionSpy).toHaveBeenCalledTimes(1);
    expect(dispatchActionSpy).toHaveBeenCalledWith(testActions.actions.rstart);
    expect(wrapper.emitted()['action-executed'])
      .toEqual([[{ action: testActions.actions.rstart, payload: undefined, ed: {}, actionHandled: false }]]);
  });

  it(
    'dispatches an action and calls the action-provided handler function that returns false for processed',
    async () => {
      const dispatchActionSpy = vi.spyOn(wrapper.vm, 'dispatchAction');
      const testActions = new FilteredActions({ head: actions.head, datum_lookup: actions.datum_lookup });
      const testAction = testActions.actions.datum_lookup;
      await wrapper.vm.dispatchAction(testAction);
      expect(dispatchActionSpy).toHaveBeenCalledTimes(1);
      expect(dispatchActionSpy).toHaveBeenCalledWith(testAction);
      expect(wrapper.emitted()['action-executed'])
        .toEqual([[{ action: testAction, payload: undefined, ed: {}, actionHandled: false }]]);
    },
  );
});
