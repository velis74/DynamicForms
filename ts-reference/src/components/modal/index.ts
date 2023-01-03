import DfModal from './modal.mixin';
import ModalView from './modal-view.mixin';

export interface DialogDefinition {
  dialogId?: number | null;
  topOfTheStack?: boolean;
  promise?: Promise<any>;
  resolvePromise?: (value: unknown) => void;
  rejectPromise?: (reason?: any) => void;
  body?: any;
  close?: Function;
  options?: any;
  actions?: any;
  title?: string
  isDfDialog?: boolean;
}

export { DfModal, ModalView };
