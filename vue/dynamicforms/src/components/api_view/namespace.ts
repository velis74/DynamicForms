import { AxiosRequestConfig } from 'axios/index';

import { APIConsumer } from '../api_consumer/namespace';

export type PrimaryKeyType = number | string;

export interface IView<T> {
  retrieve: (config?: AxiosRequestConfig) => Promise<T>
  create: (data: T, config?: AxiosRequestConfig) => Promise<T>
  update: (data: T, config?: AxiosRequestConfig) => Promise<T>
  delete: (config?: AxiosRequestConfig) => Promise<T>
}

export interface IViewApi<T> extends IView<T> {
  // TODO: type componentDefinition to appropriate type
  componentDefinition: (config?: AxiosRequestConfig) => Promise<APIConsumer.TableUXDefinition>;
}

export interface IViewSet<T> extends IView<T> {
  list: (config?: AxiosRequestConfig) => Promise<T[]>
}

export interface IViewSetApi<T> {
  // TODO: type componentDefinition to appropriate type
  componentDefinition: (pk?: PrimaryKeyType, config?: AxiosRequestConfig) => Promise<APIConsumer.TableUXDefinition>;
  list: (config?: AxiosRequestConfig) => Promise<T[]>
  retrieve: (pk: PrimaryKeyType, config?: AxiosRequestConfig) => Promise<T>
  create: (data: T, config?: AxiosRequestConfig) => Promise<T>
  update: (pk: PrimaryKeyType, data: T, config?: AxiosRequestConfig) => Promise<T>
  delete: (pk: PrimaryKeyType, config?: AxiosRequestConfig) => Promise<T>
}
