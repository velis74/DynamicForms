import { Ref } from 'vue';

import { IHandlers } from '../../actions/action-handler-composable';
import FormPayload from '../../form/definitions/form-payload';
import type { APIConsumer } from '../namespace';

import FormConsumerApi from './api';

export default async function FormConsumerApiOneShot <T = any>(
  baseUrl: string | Ref<string>,
  trailingSlash: boolean = false,
  pk?: APIConsumer.PKValueType,
  formData?: FormPayload,
  handlers?: IHandlers,
): Promise<T | undefined> {
  const formConsumer = new FormConsumerApi(baseUrl, trailingSlash, pk, handlers);

  let error = {};
  let result: T | undefined;

  let data = formData;

  do {
    // eslint-disable-next-line no-await-in-loop
    const formResult = await formConsumer.withErrors(error).execute(data);

    const resultAction = formResult.action;
    data = formResult.data;

    error = {};

    if (resultAction.action.name === 'submit') {
      try {
        // eslint-disable-next-line no-await-in-loop
        result = await formConsumer.save();
      } catch (err: any) {
        error = { ...err?.response?.data };
      }
    } else if (resultAction.action.name === 'delete_dlg') {
      try {
        // eslint-disable-next-line no-await-in-loop
        result = await formConsumer.delete();
      } catch (err: any) {
        error = { ...err.response.data };
      }
    }
    // propagate error to the next dialog
  } while (error && Object.keys(error).length);

  return result;
}
