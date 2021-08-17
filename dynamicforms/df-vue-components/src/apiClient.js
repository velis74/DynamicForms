import axios from 'axios';
import _ from 'lodash';

const MAX_GET_REQUEST_LENGHT = 2083;

const apiClient = axios.create({
  xsrfCookieName: 'csrftoken',
  xsrfHeaderName: 'X-CSRFToken',
  withCredentials: false,
});

let requestSeq = 0;

apiClient.interceptors.request.use((config) => {
  if (!config.url.includes('/dynamicforms/progress')) {
    // we don't include the progress requests themselves into the progress tracking.
    // They were too messy and caused recursion that resulted in way too many requests.
    const reqParams = window.dynamicforms.dialog.addRequest(++requestSeq);
    config.sequence = reqParams.sequence;
    config.headers['x-df-timestamp'] = config.headers['x-df-timestamp'] || reqParams.timestamp;
  }
  if (_.toLower(config.method) === 'get' && _.size(config.url) > MAX_GET_REQUEST_LENGHT &&
    _.includes(_.map(_.keys(config.headers), (v) => _.toLower(v)), 'x-viewmode')) {
    const errMsg = 'Your request exceeds maximum length';
    window.dynamicforms.dialog.message('error', errMsg);
    throw new axios.Cancel(errMsg);
  }
  return config;
});

apiClient.interceptors.response.use(
  (response) => {
    window.dynamicforms.dialog.removeRequest(response.config.sequence);
    return response;
  },
  (error) => {
    window.dynamicforms.dialog.removeRequest(error.config.sequence);
    return error;
  },
);
export default apiClient;
