import { AxiosRequestConfig } from 'axios';
import { computed, isRef, ref, Ref } from 'vue';

import { APIConsumer } from '../api_consumer/namespace';
import apiClient from '../util/api-client';

import { IDetailViewApi, PrimaryKeyType, PrimaryKeyBaseType, QueryType } from './namespace';

function urlParamToRef(url: string | Ref<string>) {
  const urlRef = isRef(url) ? url : ref(url);
  return computed(() => urlRef.value.replace(/\/+$/, ''));
}

function objectToURLEParam(obj: Partial<any> | Ref<Partial<any>>) {
  const deRef: Partial<any> = isRef(obj) ? <Partial<any>> obj.value : obj;
  return computed(() => new URLSearchParams(
    Object.fromEntries(Object.entries(deRef).map(([k, v]) => [k, v.toString()])),
  ));
}

function makeQuery(query?: QueryType): Ref<URLSearchParams> | undefined {
  if (!query) return undefined;
  if (isRef(query) && (query.value instanceof URLSearchParams)) return <Ref<URLSearchParams>> query;
  if (isRef(query)) return objectToURLEParam(query);
  if (query instanceof URLSearchParams) return ref(query);
  return objectToURLEParam(query);
}

export default class DetailViewApi<T = any> implements IDetailViewApi<T> {
  protected readonly baseUrl: Ref<string>;

  protected readonly trailingSlash: boolean;

  protected readonly pk?: Ref<PrimaryKeyBaseType>;

  protected readonly query?: Ref<URLSearchParams>;

  public readonly detail_url: Ref<string>;

  public readonly definition_url: Ref<string>;

  public readonly data_url: Ref<string>;

  constructor(url: string | Ref<string>, trailingSlash: boolean = false, pk?: PrimaryKeyType, query?: QueryType) {
    this.baseUrl = urlParamToRef(url);
    this.trailingSlash = trailingSlash;
    if (pk === undefined) {
      this.pk = pk;
    } else {
      this.pk = isRef(pk) ? pk : ref(pk);
    }
    this.query = makeQuery(query);
    this.detail_url = computed(() => (`${this.baseUrl.value}${this.pk ? `/${this.pk.value}` : ''}`));
    this.definition_url = computed(() => (`${this.detail_url.value}.componentdef`));
    this.data_url = computed(() => `${this.detail_url.value}.json`);
  }

  compose_url(url: string | Ref<string>): string {
    let res = isRef(url) ? url.value : url;
    if (this.trailingSlash) res += '/';
    if (this.query) res += `?${this.query.value.toString()}`;
    return res;
  }

  componentDefinition = async (config?: AxiosRequestConfig): Promise<APIConsumer.FormUXDefinition> => (
    (await apiClient.get(this.compose_url(this.definition_url), config)).data
  );

  /**
   * Retrieve the record.
   * @throws {AxiosError} Throws an error if the request fails.
   */
  retrieve = async (config?: AxiosRequestConfig): Promise<T> => (
    (await apiClient.get(this.compose_url(this.data_url), config)).data
  );

  /**
   * POST the resord to the backend.
   * @throws {AxiosError} Throws an error if the request fails.
   */
  create = async (data: T, config?: AxiosRequestConfig): Promise<T> => (
    (await apiClient.post(this.compose_url(this.baseUrl.value), data, config)).data
  );

  /**
   * Update the record.
   * @throws {AxiosError} Throws an error if the request fails.
   */
  update = async (data: T, config?: AxiosRequestConfig): Promise<T> => (
    (await apiClient.put(this.compose_url(this.detail_url), data, config)).data
  );

  /**
   * Delete the record.
   * @throws {AxiosError} Throws an error if the request fails.
   */
  delete = async (config?: AxiosRequestConfig): Promise<T> => (
    (await apiClient.delete(this.compose_url(this.detail_url), config)).data
  );
}
