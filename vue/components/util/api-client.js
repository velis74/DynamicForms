import axios from 'axios';
import _ from 'lodash';

import requestTracker from './request-tracker';
//
// import dynamicforms from './dynamicforms';

const MAX_GET_REQUEST_LENGHT = 2083;

const apiClient = axios.create({
  xsrfCookieName: 'csrftoken',
  xsrfHeaderName: 'X-CSRFToken',
  withCredentials: false,
});

requestTracker.apiClient = apiClient;

apiClient.interceptors.request.use((config) => {
  const showProgress = config.showProgress !== undefined ? config.showProgress : true;
  console.assert(showProgress === true || showProgress === false);
  if (!config.url.includes('/dynamicforms/progress') && !config.url.includes('unpkg.com') && showProgress) {
    // we don't include the progress requests themselves into the progress tracking.
    // They were too messy and caused recursion that resulted in way too many requests.
    const reqParams = requestTracker.addRequest();
    config.sequence = reqParams.requestId; // remember sequence for later removal from active requests
    config.headers['x-df-timestamp'] = reqParams.timestamp; // this is for backend so that it can report progress
  }
  if (_.toLower(config.method) === 'get' && _.size(config.url) > MAX_GET_REQUEST_LENGHT &&
    _.includes(_.map(_.keys(config.headers), (v) => _.toLower(v)), 'x-viewmode')) {
    const errMsg = 'Your request exceeds maximum length';
    console.error(errMsg);
    throw new axios.Cancel(errMsg);
  }
  return config;
});

apiClient.interceptors.response.use(
  (response) => {
    requestTracker.removeRequest(response.config.sequence);
    return response;
  },
  (error) => {
    requestTracker.removeRequest(error.config.sequence);
    return Promise.reject(error);
  },
);

export default apiClient;
