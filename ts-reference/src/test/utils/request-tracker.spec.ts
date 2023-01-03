import { it, describe, expect, beforeEach } from 'vitest';
import requestTracker from '@/components/util/request-tracker';
import { forEach } from 'lodash';

const tracker = requestTracker;

beforeEach(() => {
  Object.keys(tracker.activeRequests).forEach((request) => {
    tracker.removeRequest(request);
  })
});

describe('Request Tracker', () => {
  it('Add request', () => {
    const reply = tracker.addRequest();
    expect(reply).not.toBeNull();
    expect(Object.keys(tracker.activeRequests).length).equal(1);
  });
  it('Remove request', () => {
    const request = tracker.addRequest();
    tracker.removeRequest(request.requestId);
    expect(Object.keys(tracker.activeRequests).length).equal(0);
  });
  it('Oldest request', () => {
    const oldest = tracker.addRequest();
    expect(tracker.oldestActiveRequest().requestId).equal(String(oldest.requestId));
    const newer = tracker.addRequest();
    expect(tracker.oldestActiveRequest().requestId).not.equal(String(newer.requestId));
    expect(tracker.oldestActiveRequest().requestId).equal(String(oldest.requestId));
  })
});
