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
) => {
  notify({
    title,
    text,
    duration,
    id,
    type,
    data: {
      onNotificationClose: (item: any, closeFunction: any) => {
        closeFunction();
      },
    },
  });
};

const showInfoNotification = (text: string, title?: string) => {
  const resolvedTitle = title ?? gettext('Info');
  return showNotification(resolvedTitle, text, 'info');
};

const showSuccessNotification = (text: string, title?: string) => {
  const resolvedTitle = title ?? gettext('Success');
  return showNotification(resolvedTitle, text, 'success');
};

const showWarningNotification = (text: string, title?: string) => {
  const resolvedTitle = title ?? gettext('Warning');
  return showNotification(resolvedTitle, text, 'warn');
};

const showErrorNotification = (text: string, title?: string) => {
  const resolvedTitle = title ?? gettext('Error');
  return showNotification(resolvedTitle, text, 'error');
};

const showNotificationFromAxiosException = (exc: AxiosError) => {
  let text;
  const exceptionBody: string[] | string = (exc.response?.data ?? '') as (string[] | string);
  if (typeof exceptionBody === 'string') {
    text = exceptionBody;
  } else {
    text = exceptionBody.join(' ');
  }
  return showErrorNotification(text);
};

export {
  DfNotification,
  showNotification,
  showInfoNotification,
  showSuccessNotification,
  showWarningNotification,
  showErrorNotification,
  showNotificationFromAxiosException,
};
