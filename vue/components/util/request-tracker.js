class RequestTracker {
  constructor() {
    this.activeRequests = {};
    this.requestCounter = 0;
    this.apiClient = null; // type: apiClient
    this.dialogPromise = null;
    this.dfModal = null;
  }

  // this.dfModal is set when modal-view.js is executed
  get isInstalled() { return this.dfModal != null; }

  addRequest() {
    /**
     * Adds a new active request to track. If the request does not complete in 250ms, progress dialog will be shown
     */
    const requestId = ++this.requestCounter;
    this.activeRequests[requestId] = new Date().getTime();
    return { requestId, timestamp: this.activeRequests[requestId] };
  }

  removeRequest(requestId) {
    /**
     * Removes (no longer) active request from tracking. Any open progress dialogs will be hidden
     */
    if (!requestId) return; // this will be true for progress requests made by progressDialogCheck function
    delete this.activeRequests[requestId];
    this.progressDialogCheck(); // remove the progress dialog when all requests are done
  }

  loading() { return Object.keys(this.activeRequests).length; }

  get isShowingProgress() {
    return this.dfModal.isCurrentDialogPromise(this.dialogPromise);
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
    const oldest = activeRequestKeys[0];
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
    if (!this.isInstalled) return; // Don't attempt to show the dialog if the dfModal is not installed

    const oldestActiveRequest = this.oldestActiveRequest();

    if (oldestActiveRequest.age >= 250 && !this.isShowingProgress) {
      this.show();
    } else if (oldestActiveRequest.age >= 250 && this.isShowingProgress) {
      if (!this.apiClient) return;

      const progress = await this.apiClient.get(
        '/dynamicforms/progress/', { headers: { 'x-df-timestamp': oldestActiveRequest.timestamp } },
      );
      // we need to recheck because after the request, the dialog might no longer show
      if (this.isShowingProgress) {
        const dlgDef = this.dfModal.getDialogDefFromPromise(this.dialogPromise);
        dlgDef.body.props.progress = Number(progress.data.value);
        dlgDef.body.props.label = progress.data.comment;
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
    const title = 'Performing operation';
    this.dialogPromise = this.dfModal.message(
      title,
      { componentName: 'LoadingIndicator', props: { loading: true, label: null, progress: null } },
    );
  }

  hide() {
    const dlgDef = this.dfModal.getDialogDefFromPromise(this.dialogPromise);
    if (dlgDef) this.dfModal.popDialog(dlgDef.dialogId);
    this.dialogPromise = null;
  }
}

const requestTracker = new RequestTracker();
// Set up the check for progress dialogs
window.setInterval(() => { requestTracker.progressDialogCheck(); }, 250);

export default requestTracker;
