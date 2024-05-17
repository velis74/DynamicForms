import type { ActionsNS } from '../../../actions/namespace';
import { InMemoryParams } from '../../../adapters';
import FormConsumerArray from '../array';

import FormConsumerOneShotBase from './base';

type IHandlers = ActionsNS.IHandlers;

export default async function FormConsumerOneShotArray<T extends object = any>(
  params: InMemoryParams<T>,
  handlers?: IHandlers,
): Promise<T | undefined> {
  const formConsumer = new FormConsumerArray<T>(params, handlers);

  return FormConsumerOneShotBase(formConsumer);
}
