import { VNode } from 'vue';

import FilteredActions from '../actions/filtered-actions';

import { Dialogs } from './namespace';

let idGenerator = 0;

export default class DialogDefinition implements Dialogs.RunningDialog {
  /* Base dialog definition */
  public title: string | VNode;

  public body: Dialogs.DialogMessage;

  public options: Dialogs.DialogOptions;

  public actions: FilteredActions | VNode;

  public dialogId: number; // Unique dialog ID

  private _topOfTheStack?: boolean; // true when this dialog is the first one

  /*  API functions */
  public close: Function; // API function to close this dialog from calling code

  /* Support declarations */
  public promise: Promise<any>; // The promise which will be resolved when the dialog closes

  public resolvePromise: Function; // function to resolve the promise

  public rejectPromise: Function; // Function to reject the promise

  constructor(
    title: string | VNode,
    body: Dialogs.DialogMessage,
    options: Dialogs.DialogOptions,
    actions: FilteredActions,
  ) {
    this.title = title;
    this.body = body;
    this.options = options;
    this.actions = actions;
    this.dialogId = ++idGenerator;
    this.close = () => null;
    this.promise = new Promise<any>(() => {});
    this.resolvePromise = () => null;
    this.rejectPromise = () => null;
  }

  get topOfTheStack() { return this._topOfTheStack || false; }

  set topOfTheStack(value: boolean) { this._topOfTheStack = value; }
}
