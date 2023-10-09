import { APIConsumer } from '../api_consumer/namespace';

type MaybeAwaitable<T = any> = Promise<T> | T;

export interface FormAdapter<T = any> {
  componentDefinition: () => MaybeAwaitable<APIConsumer.FormUXDefinition>
  retrieve: () => MaybeAwaitable<T>
  create: (data: T) => MaybeAwaitable<T>
  update: (data: T) => MaybeAwaitable<T>
  delete: () => MaybeAwaitable<T>
}
