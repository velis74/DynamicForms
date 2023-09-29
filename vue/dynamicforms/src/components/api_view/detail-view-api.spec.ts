import MockAdapter from 'axios-mock-adapter';
import { computed, ref, nextTick } from 'vue';

import apiClient from '../util/api-client';

import DetailViewApi from './detail-view-api';

const mock = new MockAdapter(apiClient);

describe('DetailViewApi Construction', () => {
  it('should construct with only a base URL', () => {
    const api = new DetailViewApi({ url: '/api' });
    expect(api.detail_url.value).toBe('/api');
    expect(api.definition_url.value).toBe('/api.componentdef');
    expect(api.data_url.value).toBe('/api.json');
  });

  it('should construct with a base URL and trailing slash', () => {
    const api = new DetailViewApi({ url: '/api', trailingSlash: true });
    expect(api.detail_url.value).toBe('/api');
    expect(api.definition_url.value).toBe('/api.componentdef');
    expect(api.data_url.value).toBe('/api.json');
  });

  it('should construct with a base URL and primary key', () => {
    const api = new DetailViewApi({ url: '/api', trailingSlash: false, pk: '123' });
    expect(api.detail_url.value).toBe('/api/123');
    expect(api.definition_url.value).toBe('/api/123.componentdef');
    expect(api.data_url.value).toBe('/api/123.json');
  });

  it('should construct with a base URL, primary key, and query', () => {
    const api = new DetailViewApi({ url: '/api', trailingSlash: false, pk: '123', query: { key: 'value' } });
    expect(api.detail_url.value).toBe('/api/123');
    expect(api.definition_url.value).toBe('/api/123.componentdef');
    expect(api.data_url.value).toBe('/api/123.json');
  });

  it('should construct with all parameters as Refs', () => {
    const api = new DetailViewApi({
      url: computed(() => '/api'),
      trailingSlash: true,
      pk: computed(() => '123'),
      query: computed(() => new URLSearchParams('key=value')),
    });
    expect(api.detail_url.value).toBe('/api/123');
    expect(api.definition_url.value).toBe('/api/123.componentdef');
    expect(api.data_url.value).toBe('/api/123.json');
  });
});

describe('DetailViewApi', () => {
  afterEach(() => {
    mock.reset();
  });

  it('should handle retrieve correctly', async () => {
    const api = new DetailViewApi({ url: '/api' });
    mock.onGet('/api.json').reply(200, { foo: 'bar' });

    const data = await api.retrieve();
    expect(data).toEqual({ foo: 'bar' });
  });

  it('should handle create correctly', async () => {
    const api = new DetailViewApi({ url: '/api' });
    mock.onPost('/api').reply(200, { id: 1, foo: 'bar' });

    const data = await api.create({ foo: 'bar' });
    expect(data).toEqual({ id: 1, foo: 'bar' });
  });

  it('should handle update correctly', async () => {
    const api = new DetailViewApi({ url: ref('/api'), trailingSlash: false, pk: ref(1) });
    mock.onPut('/api/1').reply(200, { id: 1, foo: 'updated' });

    const data = await api.update({ foo: 'updated' });
    expect(data).toEqual({ id: 1, foo: 'updated' });
  });

  it('should handle delete correctly', async () => {
    const api = new DetailViewApi({ url: ref('/api'), trailingSlash: false, pk: ref(1) });
    mock.onDelete('/api/1').reply(200, { success: true });

    const data = await api.delete();
    expect(data).toEqual({ success: true });
  });

  it('should handle retrieve with query parameters as URLSearchParams', async () => {
    const api = new DetailViewApi({
      url: '/api',
      trailingSlash: false,
      query: new URLSearchParams({ key: 'value with space' }),
    });
    mock.onGet('/api.json?key=value+with+space').reply(200, { foo: 'bar' });
    mock.onGet('/api.componentdef?key=value+with+space').reply(200, { foo: 'definition' });

    const data = await api.retrieve();
    expect(data).toEqual({ foo: 'bar' });
    const data2 = await api.componentDefinition();
    expect(data2).toEqual({ foo: 'definition' });
  });

  it('should handle retrieve with query parameters as object', async () => {
    const api = new DetailViewApi({
      url: '/api',
      trailingSlash: false,
      query: { key: 'value with space' },
    });
    mock.onGet('/api.json?key=value+with+space').reply(200, { foo: 'bar' });

    const data = await api.retrieve();
    expect(data).toEqual({ foo: 'bar' });
  });

  it('should react to changes in pk and query parameters', async () => {
    const pk = ref('123');
    const query = ref(new URLSearchParams('key=value'));

    const api = new DetailViewApi({ url: '/api', trailingSlash: false, pk, query });

    // Initial state
    expect(api.detail_url.value).toBe('/api/123');
    expect(api.definition_url.value).toBe('/api/123.componentdef');
    expect(api.compose_url(api.data_url, true)).toBe('/api/123.json?key=value');

    // Mock for initial state
    mock.onGet('/api/123.json?key=value').reply(200, { foo: 'bar' });

    let data = await api.retrieve();
    expect(data).toEqual({ foo: 'bar' });

    // Change pk and query
    pk.value = '456';
    query.value = new URLSearchParams('newkey=newvalue');

    // Vue's reactivity is asynchronous, wait for it
    await nextTick();

    // Check updated state
    expect(api.detail_url.value).toBe('/api/456');
    expect(api.definition_url.value).toBe('/api/456.componentdef');
    expect(api.compose_url(api.data_url.value, true)).toBe('/api/456.json?newkey=newvalue');

    // Mock for updated state
    mock.reset();
    mock.onGet('/api/456.json?newkey=newvalue').reply(200, { foo: 'updated' });

    data = await api.retrieve();
    expect(data).toEqual({ foo: 'updated' });
  });
});
