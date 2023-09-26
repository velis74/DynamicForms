import MockAdapter from 'axios-mock-adapter';

import apiClient from '../../util/api-client';

import FormConsumerApiOneShot from './api-one-shot';
import data from './api-one-shot.spec.json';

const mock = new MockAdapter(apiClient);

describe('Api One Shot', () => {
  it('Create', () => {
    mock.onGet('/test.componentdef').reply(200, data);

    const consumer = FormConsumerApiOneShot({ url: '/test' });
    expectTypeOf(consumer).toEqualTypeOf(FormConsumerApiOneShot);

    mock.reset();
  });
});
