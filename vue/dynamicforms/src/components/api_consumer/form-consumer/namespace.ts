import { ActionsNS } from '../../actions/namespace';
import FormPayload from '../../form/definitions/form-payload';
import DialogDefinition from '../../modal/dialog-definition';

import FormConsumerApi from './api';

export type FormConsumerHook<T = FormConsumerApi> = (consumer: T, ...params: any[]) => any;

export interface FormResult {
  action: ActionsNS.ActionJSON
  dialog: DialogDefinition
  extraData: unknown
}

export interface FormConsumerHooks<T> {
  beforeDialog?: (instance: T, ...params: any[]) => any;
  afterDialog?: (instance: T, action: any) => void;
}

export interface FormExecuteResult {
  data: FormPayload
  action: FormResult,
}
