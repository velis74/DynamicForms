import { AxiosRequestConfig } from 'axios/index';

import { APIConsumer } from '../api_consumer/namespace';

export type PrimaryKeyType = number | string;

export interface IView<T = any> {
  retrieve: (config?: AxiosRequestConfig) => Promise<T>
  create: (data: T, config?: AxiosRequestConfig) => Promise<T>
  update: (data: T, config?: AxiosRequestConfig) => Promise<T>
  delete: (config?: AxiosRequestConfig) => Promise<T>
}

export interface IViewApi<T = any> extends IView<T> {
  componentDefinition: (config?: AxiosRequestConfig) => Promise<APIConsumer.FormUXDefinition>;
}

export interface IViewSet<T = any> extends IView<T> {
  list: (config?: AxiosRequestConfig) => Promise<T[]>
}

export interface IDetailViewApi<T = any> {
  componentDefinition: (pk?: PrimaryKeyType, config?: AxiosRequestConfig) => Promise<APIConsumer.FormUXDefinition>;
  retrieve: (pk: PrimaryKeyType, config?: AxiosRequestConfig) => Promise<T>
  create: (data: T, config?: AxiosRequestConfig) => Promise<T>
  update: (pk: PrimaryKeyType, data: T, config?: AxiosRequestConfig) => Promise<T>
  delete: (pk: PrimaryKeyType, config?: AxiosRequestConfig) => Promise<T>
}

export interface IViewSetApi<T = any> extends Omit<IDetailViewApi<T>, 'componentDefinition'> {
  componentDefinition: (pk?: PrimaryKeyType, config?: AxiosRequestConfig) => Promise<APIConsumer.TableUXDefinition>;
  list: (config?: AxiosRequestConfig) => Promise<T[]>
}
