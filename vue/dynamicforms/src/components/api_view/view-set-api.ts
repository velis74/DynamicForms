import { AxiosRequestConfig, RawAxiosRequestHeaders } from 'axios';

import { APIConsumer } from '../api_consumer/namespace';
import apiClient from '../util/api-client';

import { IViewSetApi, PrimaryKeyType } from './namespace';

export default class ViewSetApi<T> implements IViewSetApi<T> {
  protected baseUrl: string;

  protected headers: RawAxiosRequestHeaders = { 'x-viewmode': 'TABLE_ROW', 'x-pagination': 1 };

  protected trailingSlash: boolean;

  constructor(url: string, trailingSlash: boolean = false) {
    this.baseUrl = url.replace(/\/+$/, '');
    this.trailingSlash = trailingSlash;
  }

  compose_url(url: string): string {
    return this.trailingSlash ? `${url}/` : url;
  }

  // eslint-disable-next-line class-methods-use-this
  definition_url(url: string): string { return `${url}.componentdef`; }

  // eslint-disable-next-line class-methods-use-this
  data_url(url: string): string { return `${url}.json`; }

  detail_url = (pk?: PrimaryKeyType) => (pk ? `${this.baseUrl}/${pk}` : this.baseUrl);

  componentDefinition = async (
    pk?: PrimaryKeyType,
    config?: AxiosRequestConfig,
  ): Promise<APIConsumer.TableUXDefinition> => (
    (await apiClient.get(
      this.compose_url(this.definition_url(this.detail_url(pk))),
      pk ? config : { headers: this.headers, ...config },
    )).data
  );

  list = async (config?: AxiosRequestConfig): Promise<T[]> => (
    (await apiClient.get(this.compose_url(this.baseUrl), { headers: this.headers, ...config })).data
  );

  retrieve = async (pk: PrimaryKeyType, config?: AxiosRequestConfig): Promise<T> => (
    (await apiClient.get(this.compose_url(this.data_url(this.detail_url(pk))), config)).data
  );

  create = async (data: T, config?: AxiosRequestConfig): Promise<T> => (
    (await apiClient.post(`${this.baseUrl}/`, data, config)).data
  );

  update = async (pk: PrimaryKeyType, data: T, config?: AxiosRequestConfig): Promise<T> => (
    (await apiClient.put(this.compose_url(this.detail_url(pk)), data, config)).data
  );

  delete = async (pk: PrimaryKeyType, config?: AxiosRequestConfig): Promise<T> => (
    (await apiClient.delete(this.compose_url(this.detail_url(pk)), config)).data
  );
}
