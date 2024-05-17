import type { ActionsNS } from '../../actions/namespace';
import DetailViewApi from '../../adapters/api/detail-view-api';
import { DetailViewOptions } from '../../adapters/api/namespace';

import FormConsumerBase from './base';
import type { FormConsumerHooks } from './namespace';

type IHandlers = ActionsNS.IHandlers;

class FormConsumerApi<T = any> extends FormConsumerBase<T> {
  declare beforeDialog?: (consumer: FormConsumerApi, ...params: any[]) => any;

  declare afterDialog?: (instance: FormConsumerApi, action: any) => void;

  constructor(
    apiOptions: DetailViewOptions,
    actionHandlers?: IHandlers,
    hooks?: FormConsumerHooks<FormConsumerApi>,
  ) {
    super(actionHandlers, hooks);

    this.api = new DetailViewApi<T>(apiOptions);
  }
}

export default FormConsumerApi;
