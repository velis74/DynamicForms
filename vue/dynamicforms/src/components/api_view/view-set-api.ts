import { AxiosRequestConfig } from 'axios';

import apiClient from '../util/api-client';

import { IViewSetApi } from './namespace';

export default class ViewSetApi<T> implements IViewSetApi<T> {
  protected baseUrl: string;

  constructor(url: string) {
    this.baseUrl = url.replace(/\/+$/, '');
  }

  get trailing_slash_url() { return `${this.baseUrl}/`; }

  detail_url = (pk: number) => (`${this.baseUrl}/${pk}`);

  list = async (config?: AxiosRequestConfig): Promise<T[]> => (
    (await apiClient.get(this.baseUrl, config)).data
  );

  retrieve = async (pk: number, config?: AxiosRequestConfig): Promise<T> => (
    (await apiClient.get(this.detail_url(pk), config)).data
  );

  create = async (data: T, config?: AxiosRequestConfig): Promise<T> => (
    (await apiClient.post(this.trailing_slash_url, data, config)).data
  );

  update = async (pk: number, data: T, config?: AxiosRequestConfig): Promise<T> => (
    (await apiClient.put(this.detail_url(pk), data, config)).data
  );

  delete = async (pk: number, config?: AxiosRequestConfig): Promise<T> => (
    (await apiClient.delete(this.detail_url(pk), config)).data
  );
}
