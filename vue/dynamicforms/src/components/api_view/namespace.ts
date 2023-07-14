import { AxiosRequestConfig } from 'axios/index';

export type PrimaryKeyType = number;

export interface IView<T> {
  retrieve: (config?: AxiosRequestConfig) => Promise<T>
  create: (data: T, config?: AxiosRequestConfig) => Promise<T>
  update: (data: T, config?: AxiosRequestConfig) => Promise<T>
  delete: (config?: AxiosRequestConfig) => Promise<T>
}

export interface IViewSet<T> extends IView<T> {
  list: (config?: AxiosRequestConfig) => Promise<T[]>
}

export interface IViewSetApi<T> {
  list: (config?: AxiosRequestConfig) => Promise<T[]>
  retrieve: (pk: PrimaryKeyType, config?: AxiosRequestConfig) => Promise<T>
  create: (data: T, config?: AxiosRequestConfig) => Promise<T>
  update: (pk: PrimaryKeyType, data: T, config?: AxiosRequestConfig) => Promise<T>
  delete: (pk: PrimaryKeyType, config?: AxiosRequestConfig) => Promise<T>
}
