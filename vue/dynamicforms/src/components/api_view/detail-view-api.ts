import { AxiosRequestConfig } from 'axios';
import { computed, isRef, MaybeRef, ref, Ref, unref } from 'vue';

import { APIConsumer } from '../api_consumer/namespace';
import apiClient from '../util/api-client';

import {
  IDetailViewApi,
  PrimaryKeyBaseType,
  QueryType,
  DetailViewDefaults,
  DetailViewOptions,
  DetailOptionsWithDefaults,
} from './namespace';

function urlParamToRef(url: MaybeRef<string>) {
  const urlRef = ref(url);
  return computed(() => urlRef.value?.replace?.(/\/+$/, ''));
}

function objectToURLEParam(obj: MaybeRef<Partial<any>>) {
  return computed(() => new URLSearchParams(
    Object.fromEntries(Object.entries(unref(obj)).map(([k, v]) => {
      const value = typeof v === 'object' ?
        // eslint-disable-next-line eqeqeq
        JSON.stringify(Object.fromEntries(Object.entries(v).filter(([, val]) => val != undefined))) : v.toString();
      return [k, value];
    })),
  ));
}

function makeQuery(query?: QueryType): Ref<URLSearchParams> | undefined {
  if (!query) return undefined;
  if (isRef(query) && (query.value instanceof URLSearchParams)) return <Ref<URLSearchParams>> query;
  if (isRef(query)) return objectToURLEParam(query);
  if (query instanceof URLSearchParams) return ref(query);
  return objectToURLEParam(query);
}

const detailViewOptionsDefaults: DetailViewDefaults = { trailingSlash: false, useQueryInRetrieveOnly: true };

const withDefaults = (options: DetailViewOptions): DetailOptionsWithDefaults => (
  { ...detailViewOptionsDefaults, ...options }
);

export default class DetailViewApi<T = any> implements IDetailViewApi<T> {
  protected readonly baseUrl: Ref<string>;

  protected readonly trailingSlash: boolean;

  protected readonly pk?: Ref<PrimaryKeyBaseType>;

  protected readonly query?: Ref<URLSearchParams>;

  protected readonly useQueryInRetrieveOnly: boolean;

  public readonly detail_url: Ref<string>;

  public readonly definition_url: Ref<string>;

  public readonly data_url: Ref<string>;

  constructor(options: DetailViewOptions) {
    const optionsWithDefault = withDefaults(options);

    this.baseUrl = urlParamToRef(optionsWithDefault.url);
    this.trailingSlash = optionsWithDefault.trailingSlash;
    this.pk = (optionsWithDefault.pk === undefined) ? undefined : ref(optionsWithDefault.pk);
    this.query = makeQuery(optionsWithDefault.query);
    this.useQueryInRetrieveOnly = optionsWithDefault.useQueryInRetrieveOnly;

    this.detail_url = computed(() => (`${this.baseUrl.value}${this.pk ? `/${this.pk.value}` : ''}`));
    this.definition_url = computed(() => (`${this.detail_url.value}.componentdef`));
    this.data_url = computed(() => `${this.detail_url.value}.json`);
  }

  compose_url(url: string | Ref<string>, useQuery: boolean): string {
    let res = unref(url);
    if (this.trailingSlash) res += '/';
    if (this.query && useQuery) res += `?${this.query.value.toString()}`;
    return res;
  }

  componentDefinition = async (config?: AxiosRequestConfig): Promise<APIConsumer.FormUXDefinition> => (
    (await apiClient.get(this.compose_url(this.definition_url, this.useQueryInRetrieveOnly), config)).data
  );

  /**
   * Retrieve the record.
   * @throws {AxiosError} Throws an error if the request fails.
   */
  retrieve = async (config?: AxiosRequestConfig): Promise<T> => (
    (await apiClient.get(this.compose_url(this.data_url, this.useQueryInRetrieveOnly), config)).data
  );

  /**
   * POST the resord to the backend.
   * @throws {AxiosError} Throws an error if the request fails.
   */
  create = async (data: T, config?: AxiosRequestConfig): Promise<T> => (
    (await apiClient.post(this.compose_url(this.baseUrl.value, false), data, config)).data
  );

  /**
   * Update the record.
   * @throws {AxiosError} Throws an error if the request fails.
   */
  update = async (data: T, config?: AxiosRequestConfig): Promise<T> => (
    (await apiClient.put(this.compose_url(this.detail_url, false), data, config)).data
  );

  /**
   * Delete the record.
   * @throws {AxiosError} Throws an error if the request fails.
   */
  delete = async (config?: AxiosRequestConfig): Promise<T> => (
    (await apiClient.delete(this.compose_url(this.detail_url, false), config)).data
  );
}
