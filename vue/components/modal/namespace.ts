namespace Dialogs {
  import ActionsJSON = Actions.ActionsJSON;
  import ErrorsJSON = Actions.ErrorsJSON;
  import FormLayoutType = APIConsumer.FormLayoutType;
  import FormPayload = APIConsumer.FormPayload;

  export type DialogTitle = string;

  export interface DialogOptions {
    size: number; // from dialog-size.ts
    provides: { [key: string]: any };
  }

  export interface CustomComponentMessage {
    componentName: string;
    props?: {
      [key: string]: any,
      layout?: FormLayoutType,
      payload?: FormPayload,
      actions?: ActionsJSON,
      errors?: ErrorsJSON,
    };
  }

  export type DialogMessage = string | CustomComponentMessage;

  export interface RunningDialog {
    topOfTheStack: boolean; // true when this dialog is the first one
    close: unknown; // API function to close this dialog from calling code
    /* Support declarations */
    promise: Promise<any>; // The promise which will be resolved when the dialog closes
    resolvePromise: unknown; // function to resolve the promise
    rejectPromise: unknown; // Function to reject the promise
  }
}
