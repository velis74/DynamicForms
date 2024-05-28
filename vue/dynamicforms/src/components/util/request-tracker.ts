import { AxiosInstance } from 'axios';

import DialogDefinition from '../modal/dialog-definition';
import dfModal from '../modal/modal-view-api';
import { Dialogs } from '../modal/namespace';

import { gettext } from './translations-mixin';

const SHOW_DIALOG_AFTER_MS = 250;
const emptyPromise = new Promise<any>(() => {});

class RequestTracker {
  private activeRequests: { [key: number]: number };

  private requestCounter: number;

  public apiClient?: AxiosInstance;

  private dialogPromise: Promise<any>;

  constructor() {
    this.activeRequests = {};
    this.requestCounter = 0;
    // this.apiClient = null; // type: apiClient
    this.dialogPromise = emptyPromise;
  }

  addRequest() {
    /**
     * Adds a new active request to track. If the request does not complete in 250ms, progress dialog will be shown
     */
    const requestId = ++this.requestCounter;
    this.activeRequests[requestId] = new Date().getTime();
    return { requestId, timestamp: this.activeRequests[requestId] };
  }

  removeRequest(requestId: number) {
    /**
     * Removes (no longer) active request from tracking. Any open progress dialogs will be hidden
     */
    if (!requestId) return; // this will be true for progress requests made by progressDialogCheck function
    delete this.activeRequests[requestId];
    this.progressDialogCheck(); // remove the progress dialog when all requests are done
  }

  loading() { return Object.keys(this.activeRequests).length; }

  get isShowingProgress() {
    return dfModal.getDialogDefinition(this.dialogPromise) != null;
  }

  oldestActiveRequest() {
    /**
     * Reports the oldest active request's properties. All properties are null if there is no active request.
     * requestId: id of request, null if there are none
     * timestamp: creation timestamp of oldest request, null if there are none
     * age: age of oldest request in ms, null if there are none
     */
    const activeRequests = this.activeRequests;
    const activeRequestKeys = Object.keys(activeRequests);
    if (activeRequestKeys.length === 0) return { requestId: null, timestamp: null, age: null };
    const oldest = Number(activeRequestKeys[0]);
    return {
      requestId: oldest,
      timestamp: activeRequests[oldest],
      age: new Date().getTime() - activeRequests[oldest],
    };
  }

  async progressDialogCheck() {
    /**
     * checks if there are any ongoing requests that are running for 250ms or more. If that's the case, show progress
     * This method is set up to run in global window.setInterval
     */
    if (!dfModal.isInstalled) return; // Don't attempt to show the dialog if the dfModal is not installed

    const oldestActiveRequest = this.oldestActiveRequest();

    // I'm setting age to -1 if it's null. This should prevent typescript from complaining about null to number
    //  comparison and still skip all the if statements looking for appropriately aged request
    const age = oldestActiveRequest.age ? oldestActiveRequest.age : -1;

    if (age >= SHOW_DIALOG_AFTER_MS && !this.isShowingProgress) {
      this.show();
    } else if (age >= SHOW_DIALOG_AFTER_MS && this.isShowingProgress) {
      if (!this.apiClient) return;

      const progress = await this.apiClient.get(
        '/dynamicforms/progress/',
        { headers: { 'x-df-timestamp': oldestActiveRequest.timestamp } },
      );
      // we need to recheck because after the request, the dialog might no longer show
      if (this.isShowingProgress) {
        // we are showing so getDialogDefinition will not return null here
        const dlgDef = dfModal.getDialogDefinition(this.dialogPromise) as DialogDefinition;
        const body = dlgDef.body as Dialogs.CustomComponentMessage;
        if (body.props != null) {
          body.props.progress = Number(progress.data.value);
          body.props.label = progress.data.comment;
        }
      }
    } else if (this.loading() === 0 && this.isShowingProgress) {
      this.hide();
    }
  }

  show() {
    console.log(
      `Showing progress: We have ${this.loading()} active requests to server oldest is ` +
      `${this.oldestActiveRequest().age}ms old with timestamp ${this.oldestActiveRequest().timestamp}.`,
    );
    const title = gettext('Performing operation');
    this.dialogPromise = dfModal.message(
      title,
      { componentName: 'LoadingIndicator', props: { loading: true, label: null, progress: null } },
    );
  }

  hide() {
    const dlgDef = dfModal.getDialogDefinition(this.dialogPromise);
    if (dlgDef != null) (<Function> dlgDef.close)();
    this.dialogPromise = emptyPromise;
  }
}

const requestTracker = new RequestTracker();
// Set up the check for progress dialogs
window.setInterval(() => { requestTracker.progressDialogCheck(); }, 250);

export default requestTracker;
