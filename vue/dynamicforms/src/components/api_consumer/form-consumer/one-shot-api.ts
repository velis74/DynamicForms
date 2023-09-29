import { IHandlers } from '../../actions/action-handler-composable';
import { DetailViewOptions } from '../../api_view/namespace';

import FormConsumerApi from './api';
import FormConsumerOneShotBase from './one-shot-base';

export default async function FormConsumerApiOneShot <T = any>(
  apiOptions: DetailViewOptions,
  handlers?: IHandlers,
): Promise<T | undefined> {
  const formConsumer = new FormConsumerApi<T>(apiOptions, handlers);

  return FormConsumerOneShotBase(formConsumer);
}
