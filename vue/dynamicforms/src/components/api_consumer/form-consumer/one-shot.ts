import { IHandlers } from '../../actions/action-handler-composable';

import FormConsumerArray, { InMemoryParams } from './array';
import FormConsumerOneShotBase from './one-shot-base';

export default async function FormConsumerOneShot<T = any>(
  params: InMemoryParams,
  handlers?: IHandlers,
): Promise<T | undefined> {
  const formConsumer = new FormConsumerArray<T>(params, handlers);

  return FormConsumerOneShotBase(formConsumer);
}
