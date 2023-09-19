import { AxiosRequestConfig } from 'axios';
import { computed, isRef, ref, Ref } from 'vue';

import { APIConsumer } from '../api_consumer/namespace';
import apiClient from '../util/api-client';

import { IDetailViewApi, PrimaryKeyType, PrimaryKeyBaseType } from './namespace';

function urlParamToRef(url: string | Ref<string>) {
  const urlRef = isRef(url) ? url : ref(url);
  return computed(() => urlRef.value.replace(/\/+$/, ''));
}

export default class DetailViewApi<T = any> implements IDetailViewApi<T> {
  protected baseUrl: Ref<string>;

  protected trailingSlash: boolean;

  protected pk?: Ref<PrimaryKeyBaseType>;

  private detail_url: Ref<string>;

  private definition_url: Ref<string>;

  private data_url: Ref<string>;

  constructor(url: string | Ref<string>, trailingSlash: boolean = false, pk?: PrimaryKeyType) {
    this.baseUrl = urlParamToRef(url);
    this.trailingSlash = trailingSlash;
    if (pk === undefined) this.pk = pk;
    else this.pk = isRef(pk) ? pk : ref(pk);
    this.detail_url = computed(() => (`${this.baseUrl.value}${this.pk ? `/${this.pk.value}` : ''}`));
    this.definition_url = computed(() => (`${this.detail_url.value}.componentdef`));
    this.data_url = computed(() => `${this.detail_url.value}.json`);
  }

  compose_url(url: string | Ref<string>): string {
    const urrl = isRef(url) ? url.value : url;
    return this.trailingSlash ? `${urrl}/` : urrl;
  }

  componentDefinition = async (config?: AxiosRequestConfig): Promise<APIConsumer.FormUXDefinition> => (
    (await apiClient.get(this.compose_url(this.definition_url), config)).data
  );

  retrieve = async (config?: AxiosRequestConfig): Promise<T> => (
    (await apiClient.get(this.compose_url(this.data_url), config)).data
  );

  create = async (data: T, config?: AxiosRequestConfig): Promise<T> => (
    (await apiClient.post(this.compose_url(this.baseUrl.value), data, config)).data
  );

  update = async (data: T, config?: AxiosRequestConfig): Promise<T> => (
    (await apiClient.put(this.compose_url(this.detail_url), data, config)).data
  );

  delete = async (config?: AxiosRequestConfig): Promise<T> => (
    (await apiClient.delete(this.compose_url(this.detail_url), config)).data
  );
}
