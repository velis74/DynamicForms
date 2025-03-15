import { AxiosRequestConfig, RawAxiosRequestHeaders } from 'axios';
import { computed, isRef, ref, Ref } from 'vue';

import { APIConsumer } from '../../api_consumer/namespace';

import { IViewSetApi, PrimaryKeyType } from './namespace';

import { apiClient, dataWithResponse } from '@/util';

function urlParamToRef(url: string | Ref<string>) {
  const urlRef = isRef(url) ? url : ref(url);
  return computed(() => urlRef.value.replace(/\/+$/, ''));
}

export default class ViewSetApi<T> implements IViewSetApi<T> {
  protected baseUrl: Ref<string>;

  protected headers: RawAxiosRequestHeaders = { 'x-viewmode': 'TABLE_ROW', 'x-pagination': 1 };

  protected trailingSlash: boolean;

  constructor(url: string | Ref<string>, trailingSlash: boolean = false) {
    this.baseUrl = urlParamToRef(url);
    this.trailingSlash = trailingSlash;
  }

  compose_url(url: string): string {
    return this.trailingSlash ? `${url}/` : url;
  }

  // eslint-disable-next-line class-methods-use-this
  definition_url(url: string): string { return `${url}.componentdef`; }

  // eslint-disable-next-line class-methods-use-this
  data_url(url: string): string { return `${url}.json`; }

  detail_url = (pk?: PrimaryKeyType) => (`${this.baseUrl.value}${pk ? `/${pk}` : ''}`);

  componentDefinition = async (
    pk?: PrimaryKeyType,
    config?: AxiosRequestConfig,
  ): Promise<APIConsumer.TableUXDefinition> => (
    (await apiClient.get(
      this.compose_url(this.definition_url(this.detail_url(pk))),
      pk ? config : { headers: this.headers, ...config },
    )).data
  );

  list = async (config?: AxiosRequestConfig): Promise<T[]> => {
    const res = await apiClient.get(this.compose_url(this.baseUrl.value), { headers: this.headers, ...config });
    return { ...res.data, '$response-object': res };
  };

  retrieve = async (pk: PrimaryKeyType, config?: AxiosRequestConfig): Promise<T> => (
    dataWithResponse(await apiClient.get(this.compose_url(this.data_url(this.detail_url(pk))), config))
  );

  create = async (data: T, config?: AxiosRequestConfig): Promise<T> => (
    dataWithResponse(await apiClient.post(this.compose_url(this.baseUrl.value), data, config))
  );

  update = async (pk: PrimaryKeyType, data: T, config?: AxiosRequestConfig): Promise<T> => (
    dataWithResponse(await apiClient.put(this.compose_url(this.detail_url(pk)), data, config))
  );

  delete = async (pk: PrimaryKeyType, config?: AxiosRequestConfig): Promise<T> => (
    dataWithResponse(await apiClient.delete(this.compose_url(this.detail_url(pk)), config))
  );
}
