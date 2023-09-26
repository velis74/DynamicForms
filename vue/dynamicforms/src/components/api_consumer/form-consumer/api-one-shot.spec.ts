import MockAdapter from 'axios-mock-adapter';

import apiClient from '../../util/api-client';

import FormConsumerApiOneShot from './api-one-shot';
import data from './api-one-shot.spec.json';

const mock = new MockAdapter(apiClient);

let emitted = false;

const waitForEmitted = async () => Promise.race([async () => {
  // eslint-disable-next-line no-constant-condition
  while (true) {
    if (emitted) { return; }
    // eslint-disable-next-line no-await-in-loop
    await null;
  }
}, new Promise((resolve) => { setTimeout(resolve, 300); })]);

const replyFn = vi.fn(() => {
  emitted = true;
  return [200, data];
});

describe('Api One Shot', () => {
  afterEach(() => {
    mock.reset();
    emitted = false;
  });

  it('Create', async () => {
    mock.onGet('/test.componentdef').reply(replyFn);

    FormConsumerApiOneShot({ url: '/test' });

    // wait for api call
    await waitForEmitted();

    expect(emitted).toBe(true);
    expect(replyFn).toBeCalled();
  });
});
