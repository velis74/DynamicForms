import requestTracker from './request-tracker';

describe('RequestTracker', () => {
  afterEach(() => {
    // This will clean up the state after each test.
    Object.keys(requestTracker.activeRequests).forEach((requestId) => {
      requestTracker.removeRequest(Number(requestId));
    });
  });

  it('addRequest adds a request', () => {
    const requestInfo = requestTracker.addRequest();

    expect(requestTracker.loading()).toBe(1);
    expect(requestTracker.activeRequests[requestInfo.requestId]).toBe(requestInfo.timestamp);
  });

  it('removeRequest removes a request', () => {
    const requestInfo = requestTracker.addRequest();

    requestTracker.removeRequest(requestInfo.requestId);

    expect(requestTracker.loading()).toBe(0);
    expect(requestTracker.activeRequests[requestInfo.requestId]).toBeUndefined();
  });

  it('oldestActiveRequest returns correct information', () => {
    const firstRequestInfo = requestTracker.addRequest(); // first request
    while (new Date().getTime() <= firstRequestInfo.timestamp) ;
    const secondRequestInfo = requestTracker.addRequest(); // second request

    const oldestActiveRequest = requestTracker.oldestActiveRequest();

    expect(oldestActiveRequest.requestId).toBe(firstRequestInfo.requestId);
    expect(oldestActiveRequest.timestamp).toBe(firstRequestInfo.timestamp);
    expect(oldestActiveRequest.requestId).not.toBe(secondRequestInfo.requestId);
    expect(oldestActiveRequest.timestamp).not.toBe(secondRequestInfo.timestamp);
  });
});
