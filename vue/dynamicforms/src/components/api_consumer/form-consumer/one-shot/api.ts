import { IHandlers } from '../../../actions/action-handler-composable';
import { DetailViewOptions } from '../../../adapters/api/namespace';
import FormConsumerApi from '../api';

import FormConsumerOneShotBase from './base';

export default async function FormConsumerOneShotApi<T extends object = any>(
  apiOptions: DetailViewOptions,
  handlers?: IHandlers,
): Promise<T | undefined> {
  const formConsumer = new FormConsumerApi<T>(apiOptions, handlers);

  return FormConsumerOneShotBase(formConsumer);
}
