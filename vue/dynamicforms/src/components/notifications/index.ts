import { notify } from '@kyvg/vue3-notification';
import { AxiosError } from 'axios';

import { gettext } from '../util/translations-mixin';

import DfNotification from './df-notifications.vue';

const showNotification = (
  title: string,
  text: string,
  type = 'info',
  duration: number | undefined = undefined,
  id: number | undefined = undefined,
  data: object | undefined = {
    onNotificationClose: (item: any, closeFunction: any) => {
      closeFunction();
    },
  },
) => {
  notify({
    title,
    text,
    duration,
    id,
    type,
    data,
  });
};

const showInfoNotification = (text: string, title?: string, duration?: number, id?: number, data?: object) => {
  const resolvedTitle = title ?? gettext('Info');
  return showNotification(resolvedTitle, text, 'info', duration, id, data);
};

const showSuccessNotification = (text: string, title?: string, duration?: number, id?: number, data?: object) => {
  const resolvedTitle = title ?? gettext('Success');
  return showNotification(resolvedTitle, text, 'success', duration, id, data);
};

const showWarningNotification = (text: string, title?: string, duration?: number, id?: number, data?: object) => {
  const resolvedTitle = title ?? gettext('Warning');
  return showNotification(resolvedTitle, text, 'warn', duration, id, data);
};

const showErrorNotification = (text: string, title?: string, duration?: number, id?: number, data?: object) => {
  const resolvedTitle = title ?? gettext('Error');
  return showNotification(resolvedTitle, text, 'error', duration, id, data);
};

const showNotificationFromAxiosException = (exc: AxiosError, duration?: number, id?: number, data?: object) => {
  let text;
  const exceptionBody: string[] | string = (exc.response?.data ?? '') as (string[] | string);
  if (typeof exceptionBody === 'string') {
    text = exceptionBody;
  } else {
    text = exceptionBody.join(' ');
  }
  return showErrorNotification(text, undefined, duration, id, data);
};

const closeNotification = (id: number) => {
  notify.close(id);
};

export {
  DfNotification,
  closeNotification,
  showNotification,
  showInfoNotification,
  showSuccessNotification,
  showWarningNotification,
  showErrorNotification,
  showNotificationFromAxiosException,
};
