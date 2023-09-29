import { ActionsNS } from '../../actions/namespace';
import DialogDefinition from '../../modal/dialog-definition';

export interface FormResult {
  action: ActionsNS.ActionJSON
  dialog: DialogDefinition
  extraData: unknown
}

export interface FormConsumerHooks<T> {
  beforeDialog?: (instance: T, ...params: any[]) => any;
  afterDialog?: (instance: T, action: any) => void;
}

export interface FormExecuteResult<T = any> {
  data: Partial<T>,
  action: FormResult,
}
