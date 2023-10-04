import { AxiosRequestConfig } from 'axios/index';
import { MaybeRef } from 'vue';

import { APIConsumer } from '../../api_consumer/namespace';
import { FormAdapter } from '../namespace';

export type PrimaryKeyBaseType = number | string;
export type PrimaryKeyType = MaybeRef<PrimaryKeyBaseType>;

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
  componentDefinition: (config?: AxiosRequestConfig) => Promise<APIConsumer.FormUXDefinition>;
  retrieve: (config?: AxiosRequestConfig) => Promise<T>
  create: (data: T, config?: AxiosRequestConfig) => Promise<T>
  update: (data: T, config?: AxiosRequestConfig) => Promise<T>
  delete: (config?: AxiosRequestConfig) => Promise<T>
}

export interface IViewSetApi<T = any> {
  componentDefinition: (pk?: PrimaryKeyType, config?: AxiosRequestConfig) => Promise<APIConsumer.TableUXDefinition>;
  list: (config?: AxiosRequestConfig) => Promise<T[]>
  retrieve: (pk: PrimaryKeyType, config?: AxiosRequestConfig) => Promise<T>
  create: (data: T, config?: AxiosRequestConfig) => Promise<T>
  update: (pk: PrimaryKeyType, data: T, config?: AxiosRequestConfig) => Promise<T>
  delete: (pk: PrimaryKeyType, config?: AxiosRequestConfig) => Promise<T>
}

export type QueryBaseType = URLSearchParams | Partial<any>;
export type QueryType = MaybeRef<QueryBaseType>;

export interface DetailViewOptions {
  url: MaybeRef<string>,
  trailingSlash?: boolean
  pk?: PrimaryKeyType,
  query?: QueryType,
  useQueryInRetrieveOnly?: boolean
}

export type DetailViewDefaults = Required<Pick<DetailViewOptions, 'trailingSlash' | 'useQueryInRetrieveOnly'>>;

export type DetailOptionsWithDefaults = DetailViewOptions & DetailViewDefaults;
