import { IHandlers } from '../../actions/action-handler-composable';
import { DetailViewOptions } from '../../api_view/namespace';
import FormPayload from '../../form/definitions/form-payload';

import FormConsumerApi from './api';

export default async function FormConsumerApiOneShot <T = any>(
  apiOptions: DetailViewOptions,
  handlers?: IHandlers,
): Promise<T | undefined> {
  const formConsumer = new FormConsumerApi(apiOptions, handlers);

  let error = {};
  let result: T | undefined;

  let data: FormPayload | undefined;

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
