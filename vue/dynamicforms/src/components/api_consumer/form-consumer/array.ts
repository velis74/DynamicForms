import type { ActionsNS } from '../../actions/namespace';
import InMemoryImplementation, { InMemoryParams } from '../../adapters';

import FormConsumerBase from './base';
import type { FormConsumerHooks } from './namespace';

type IHandlers = ActionsNS.IHandlers;

export default class FormConsumerArray<T extends object = any> extends FormConsumerBase<T> {
  declare beforeDialog?: (instance: FormConsumerArray) => void;

  declare afterDialog?: (instance: FormConsumerArray, action: any) => void;

  constructor(
    params: InMemoryParams<T>,
    actionHandlers?: IHandlers,
    hooks?: FormConsumerHooks<FormConsumerArray>,
  ) {
    super(actionHandlers, hooks);

    this.api = new InMemoryImplementation<T>(params);
  }
}
