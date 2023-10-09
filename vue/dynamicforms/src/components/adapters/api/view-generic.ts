import { AxiosRequestConfig } from 'axios';

import apiClient from '../../util/api-client';

import { IView } from './namespace';

export default class ViewGeneric<T> implements IView<T> {
  protected get_url: string;

  protected post_url: string;

  protected update_url: string;

  protected delete_url: string;

  constructor(get_url: string, post_url: string, update_url: string, delete_url: string) {
    this.get_url = get_url;
    this.post_url = post_url;
    this.update_url = update_url;
    this.delete_url = delete_url;
  }

  retrieve = async (config?: AxiosRequestConfig): Promise<T> => (
    (await apiClient.get(this.get_url, config)).data
  );

  create = async (data: T, config?: AxiosRequestConfig): Promise<T> => (
    (await apiClient.post(this.post_url, data, config)).data
  );

  update = async (data: T, config?: AxiosRequestConfig): Promise<T> => (
    (await apiClient.put(this.update_url, data, config)).data
  );

  delete = async (config?: AxiosRequestConfig): Promise<T> => (
    (await apiClient.delete(this.delete_url, config)).data
  );
}
