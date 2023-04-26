import { Slot } from 'vue';

import type { Actions } from '../actions/namespace';
import type { APIConsumer } from '../api_consumer/namespace';

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
      layout?: APIConsumer.FormLayoutType,
      payload?: APIConsumer.FormPayload,
      actions?: Actions.ActionsJSON,
      errors?: Actions.ErrorsJSON,
    };
  }

  export type DialogMessage = string | CustomComponentMessage | Slot;

  export interface RunningDialog {
    topOfTheStack: boolean; // true when this dialog is the first one
    close: Function; // API function to close this dialog from calling code
    /* Support declarations */
    promise: Promise<any>; // The promise which will be resolved when the dialog closes
    resolvePromise: Function; // function to resolve the promise
    rejectPromise: Function; // Function to reject the promise
  }
}
