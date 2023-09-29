import { IHandlers } from '../../../actions/action-handler-composable';
import FormConsumerArray, { InMemoryParams } from '../array';

import FormConsumerOneShotBase from './base';

export default async function FormConsumerOneShotArray<T = any>(
  params: InMemoryParams,
  handlers?: IHandlers,
): Promise<T | undefined> {
  const formConsumer = new FormConsumerArray<T>(params, handlers);

  return FormConsumerOneShotBase(formConsumer);
}
