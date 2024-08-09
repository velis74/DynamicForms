import axios, { AxiosProgressEvent, AxiosRequestConfig, AxiosResponse } from 'axios';
import _ from 'lodash';

import requestTracker from './request-tracker';

const MAX_GET_REQUEST_LENGHT = 2083;

const apiClient = axios.create({
  xsrfCookieName: 'csrftoken',
  xsrfHeaderName: 'X-CSRFToken',
});

requestTracker.apiClient = apiClient;

declare module 'axios' {
  export interface AxiosRequestConfig {
    showProgress?: boolean;
    sequence?: number;
  }
}

export function dataWithResponse(response: AxiosResponse<any, any>) {
  const res = response.data;
  if (res) {
    Object.defineProperty(
      res,
      '$response-object',
      { get() { return response; }, enumerable: false, configurable: false },
    );
  }
  return res;
}

apiClient.interceptors.request.use((config) => {
  const showProgress = config.showProgress ?? true;

  // @ts-ignore: headers might be undefined, but they are not
  config.headers['x-df-axios'] = 'axios'; // this one is needed for vite dev server proxy

  if (!config.url?.includes('/dynamicforms/progress') && !config.url?.includes('unpkg.com') && showProgress) {
    // we don't include the progress requests themselves into the progress tracking.
    // They were too messy and caused recursion that resulted in way too many requests.
    const reqParams = requestTracker.addRequest();
    config.sequence = reqParams.requestId; // remember sequence for later removal from active requests
    // @ts-ignore: headers might be undefined, but they are not
    config.headers['x-df-timestamp'] = reqParams.timestamp; // this is for backend so that it can report progress
  }
  if (_.toLower(config.method) === 'get' && _.size(config.url) > MAX_GET_REQUEST_LENGHT &&
    _.includes(_.map(_.keys(config.headers), (v) => _.toLower(v)), 'x-viewmode')) {
    const errMsg = 'Your request exceeds maximum length';
    console.error(errMsg);
    new AbortController().abort(errMsg);
  }
  return config;
});

apiClient.interceptors.response.use(
  (response) => {
    requestTracker.removeRequest((response.config as AxiosRequestConfig).sequence as number);
    return response;
  },
  (error) => {
    requestTracker.removeRequest(error.config.sequence);
    return Promise.reject(error);
  },
);

export interface DfAxiosProgressEvent extends AxiosProgressEvent {
  computable?: boolean
}

export default apiClient;
