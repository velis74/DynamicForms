import MockAdapter from 'axios-mock-adapter';
import { ref } from 'vue';

import apiClient from '../../util/api-client';

import FormConsumerApi from './api';
import data from './api.spec.json';

const mock = new MockAdapter(apiClient);

const testUrl = '/test';

const pk = ref<number>(1);

describe('Form Consumer API', () => {
  afterEach(() => {
    mock.reset();
  });

  it('Create', () => {
    const consumer = new FormConsumerApi({ url: testUrl });
    expectTypeOf(consumer).toMatchTypeOf<FormConsumerApi>();
  });

  it('Delete', async () => {
    const replyFn = vi.fn(() => [200, data]);

    const deleteFn = vi.fn(() => [200]);

    mock.onGet('/test/1.componentdef').reply(replyFn);
    mock.onDelete('/test/1').reply(deleteFn);
    const consumer = new FormConsumerApi({ url: testUrl, pk });
    await expect(consumer.delete).rejects.toThrow();

    expect(replyFn.mock.calls.length).toBe(0);
    await consumer.getUXDefinition();
    expect(replyFn.mock.calls.length).toBe(1);

    await expect(consumer.delete()).resolves.not.toThrow();
    expect(deleteFn.mock.calls.length).toBe(1);
  });
});
