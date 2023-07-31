import { mount, shallowMount } from '@vue/test-utils';
import { vi } from 'vitest';
import { defineComponent, h } from 'vue';

import Action from './action';
import { useActionHandler } from './action-handler-composable';
import FilteredActions from './filtered-actions';

let level = 0;

const actionName = 'handle';

const action = new Action({
  name: actionName,
  label: actionName,
  position: 'ROW-END',
});

const filteredAction = new FilteredActions({
  actionName: action,
  notRelated: new Action({ name: 'notRelated', label: 'notRelated', position: 'ROW-END' }),
});

const handlers = {
  levelOne: () => { level = 1; return false; },
  levelTwo: () => { level = 2; return false; },
  levelThree: () => { level = 3; return true; },
};

// eslint-disable-next-line vue/one-component-per-file
const actionComponent = defineComponent({
  // eslint-disable-next-line vue/require-prop-types
  props: ['name', 'handleFunction'],
  setup() {
    const { handler } = useActionHandler();
    return { handler };
  },
  mounted() {
    this.handler.register('handle', this.handleFunction);
  },
  methods: {
    async callHandler() {
      await this.handler.call(action, {});
    },
  },
  template: `
    <div>
      <button type="button" :id="name" @click="callHandler"/>
      <slot></slot>
    </div>
  `,
});

// eslint-disable-next-line vue/one-component-per-file
const levelOneAction = defineComponent({
  setup() {
    const { handler } = useActionHandler(false);
    return { handler };
  },
  mounted() {
    this.handler.register('handle', handlers.levelOne);
  },
  methods: {
    async callHandler() {
      await this.handler.call(action, {});
    },
  },
  template: `
    <div>
      <button type="button" id="one" @click="callHandler"/>
      <slot></slot>
    </div>
  `,
});

// eslint-disable-next-line vue/one-component-per-file
const levelTwoAction = defineComponent({
  setup() {
    const { callHandler, registerHandler } = useActionHandler();
    return { callHandler, registerHandler };
  },
  mounted() {
    this.registerHandler('handle', handlers.levelTwo);
  },
  methods: {
    async call() {
      await this.callHandler(filteredAction, {});
    },
  },
  template: `
    <div>
      <button type="button" id="two" @click="call"/>
      <slot></slot>
    </div>
  `,
});

// eslint-disable-next-line vue/one-component-per-file
const levelThreeAction = defineComponent({
  setup() {
    const { handler } = useActionHandler();
    return { handler };
  },
  mounted() {
    this.handler.register('handle', handlers.levelThree);
  },
  methods: {
    async callHandler() {
      await this.handler.call(action, {});
    },
  },
  template: `
    <div>
      <button type="button" id="three" @click="callHandler"/>
      <slot></slot>
    </div>
  `,
});

// eslint-disable-next-line vue/one-component-per-file
const actionComponentEmpty = defineComponent({
  // eslint-disable-next-line vue/require-prop-types
  setup() {
    const { handler } = useActionHandler();
    return { handler };
  },
  methods: {
    async callHandler() {
      await this.handler.call(action, {});
    },
  },
  template: `
    <div>
      <button type="button" id="none" @click="callHandler"/>
      <slot/>
    </div>
  `,
});

let spyOne = vi.spyOn(handlers, 'levelOne');
let spyTwo = vi.spyOn(handlers, 'levelTwo');
let spyThree = vi.spyOn(handlers, 'levelThree');

describe('Action Handler', () => {
  beforeEach(() => {
    level = 0;
    spyOne = vi.spyOn(handlers, 'levelOne');
    spyTwo = vi.spyOn(handlers, 'levelTwo');
    spyThree = vi.spyOn(handlers, 'levelThree');
  });

  it('Creating action handler', async () => {
    const wrapper = shallowMount(actionComponent, { props: { name: 'one', handleFunction: handlers.levelOne } });
    await wrapper.find('#one').trigger('click');

    expect(spyOne).toBeCalled();
    expect(spyOne).toBeCalledTimes(1);
    expect(level).toBe(1);
  });

  it('Calling empty action handler', async () => {
    const wrapper = shallowMount(actionComponentEmpty);
    await wrapper.find('#none').trigger('click');

    expect(spyOne).not.toBeCalled();
    expect(level).toBe(0);
  });

  it('Nest 2 action components', async () => {
    const wrapper = mount(levelTwoAction, { slots: { default: () => h(levelOneAction) } });

    await wrapper.find('#one').trigger('click');

    expect(spyOne).not.toBeCalled();
    expect(spyTwo).toBeCalled();
    expect(level).toBe(2);

    await wrapper.find('#two').trigger('click');

    expect(spyOne).toBeCalledTimes(1);
    expect(spyTwo).toBeCalledTimes(2);
    expect(level).toBe(2);
  });

  it('Nest action components when inner component resolves', async () => {
    const wrapper = mount(levelTwoAction, { slots: { default: () => h(levelThreeAction) } });

    await wrapper.find('#three').trigger('click');

    expect(spyThree).toBeCalled();
    expect(spyTwo).not.toBeCalled();
    expect(level).toBe(3);

    await wrapper.find('#two').trigger('click');

    expect(spyThree).toBeCalledTimes(1);
    expect(spyTwo).toBeCalledTimes(1);
    expect(level).toBe(2);
  });

  it('Nest actions with none registering component', async () => {
    const wrapper = mount(levelTwoAction, { slots: { default: () => h(actionComponentEmpty) } });

    await wrapper.find('#none').trigger('click');

    expect(spyTwo).toBeCalled();
    expect(level).toBe(2);

    await wrapper.find('#two').trigger('click');

    expect(spyTwo).toBeCalledTimes(2);
    expect(level).toBe(2);
  });
});
