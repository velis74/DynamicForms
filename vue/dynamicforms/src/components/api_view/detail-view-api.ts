import { AxiosRequestConfig } from 'axios';
import { computed, isRef, ref, Ref } from 'vue';

import { APIConsumer } from '../api_consumer/namespace';
import apiClient from '../util/api-client';

import { IDetailViewApi, PrimaryKeyType } from './namespace';

function urlParamToRef(url: string | Ref<string>) {
  const urlRef = isRef(url) ? url : ref(url);
  return computed(() => urlRef.value.replace(/\/+$/, ''));
}

export default class DetailViewApi<T = any> implements IDetailViewApi<T> {
  protected baseUrl: Ref<string>;

  protected trailingSlash: boolean;

  protected pk?: PrimaryKeyType;

  constructor(url: string | Ref<string>, trailingSlash: boolean = false, pk?: PrimaryKeyType) {
    this.baseUrl = urlParamToRef(url);
    this.trailingSlash = trailingSlash;
    this.pk = pk;
  }

  compose_url(url: string): string {
    return this.trailingSlash ? `${url}/` : url;
  }

  // eslint-disable-next-line class-methods-use-this
  definition_url(url: string): string { return `${url}.componentdef`; }

  // eslint-disable-next-line class-methods-use-this
  data_url(url: string): string { return `${url}.json`; }

  detail_url = (pk?: PrimaryKeyType) => (`${this.baseUrl.value}${pk ? `/${pk}` : ''}`);

  componentDefinition = async (config?: AxiosRequestConfig): Promise<APIConsumer.FormUXDefinition> => (
    (await apiClient.get(this.compose_url(this.definition_url(this.detail_url(this.pk))), config)).data
  );

  retrieve = async (config?: AxiosRequestConfig): Promise<T> => (
    (await apiClient.get(this.compose_url(this.data_url(this.detail_url(this.pk))), config)).data
  );

  create = async (data: T, config?: AxiosRequestConfig): Promise<T> => (
    (await apiClient.post(this.compose_url(this.baseUrl.value), data, config)).data
  );

  update = async (data: T, config?: AxiosRequestConfig): Promise<T> => (
    (await apiClient.put(this.compose_url(this.detail_url(this.pk)), data, config)).data
  );

  delete = async (config?: AxiosRequestConfig): Promise<T> => (
    (await apiClient.delete(this.compose_url(this.detail_url(this.pk)), config)).data
  );
}
