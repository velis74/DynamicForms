import { RenderFunction, Slot, VNode } from 'vue';

import type { Actions } from '../actions/namespace';
import type FormPayload from '../form/definitions/form-payload';
import { DfForm } from '../form/namespace';

export namespace Dialogs {

  export type DialogTitle = string;

  export interface DialogOptions {
    size: number; // from dialog-size.ts
    // provides: { [key: string]: any }; // Jure 16.3.2023 - I have no idea what this is. Can't find any code. remove!
  }

  export interface CustomComponentMessage {
    componentName: string;
    props?: {
      [key: string]: any,
      layout?: DfForm.FormLayoutJSON,
      payload?: FormPayload,
      actions?: Actions.ActionsJSON,
      errors?: Actions.ErrorsJSON,
    };
  }

  export type DialogSectionContent = string | Slot | RenderFunction | VNode;
  export type DialogMessage = DialogSectionContent | CustomComponentMessage;

  export interface RunningDialog {
    topOfTheStack: boolean; // true when this dialog is the first one
    close: Function; // API function to close this dialog from calling code
    /* Support declarations */
    promise: Promise<any>; // The promise which will be resolved when the dialog closes
    resolvePromise: Function; // function to resolve the promise
    rejectPromise: Function; // Function to reject the promise
  }
}
