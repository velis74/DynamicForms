import { InMemoryParams } from '../../../../dist/components/api_consumer/form-consumer/array';
import { IHandlers } from '../../actions/action-handler-composable';
import InMemoryImplementation from '../../adapters';

import FormConsumerBase from './base';
import type { FormConsumerHooks } from './namespace';

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
