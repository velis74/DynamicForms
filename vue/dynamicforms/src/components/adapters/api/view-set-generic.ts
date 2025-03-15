import { AxiosRequestConfig } from 'axios';

import { IViewSet } from './namespace';
import ViewGeneric from './view-generic';

import { apiClient } from '@/util';

export default class ViewSetGeneric<T> extends ViewGeneric<T> implements IViewSet<T> {
  protected list_url: string;

  constructor(list_url: string, get_url: string, post_url: string, update_url: string, delete_url: string) {
    super(get_url, post_url, update_url, delete_url);
    this.list_url = list_url;
  }

  list = async (config: AxiosRequestConfig | undefined): Promise<T[]> => (
    (await apiClient.get(this.list_url, config)).data
  );
}
