import type { ActionsNS } from '../../../actions/namespace';
import { DetailViewOptions } from '../../../adapters/api/namespace';
import FormConsumerApi from '../api';

import FormConsumerOneShotBase from './base';

type IHandlers = ActionsNS.IHandlers;

export default async function FormConsumerOneShotApi<T extends object = any>(
  apiOptions: DetailViewOptions,
  handlers?: IHandlers,
): Promise<T | undefined> {
  const formConsumer = new FormConsumerApi<T>(apiOptions, handlers);

  return FormConsumerOneShotBase(formConsumer);
}
