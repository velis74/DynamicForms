import FormConsumerBase from '../base';

export default async function FormConsumerOneShotBase<T extends object>(
  formConsumer: FormConsumerBase<T>,
): Promise<T | undefined> {
  let error = {};
  let result: T | undefined;
  let data: Partial<T> | undefined;

  await formConsumer.getUXDefinition();

  do {
    // eslint-disable-next-line no-await-in-loop
    const formResult = await formConsumer.withErrors(error).execute(data);

    const resultAction = formResult.action;
    data = formResult.data;

    error = {};

    if (resultAction.action.name === 'submit') {
      try {
        // eslint-disable-next-line no-await-in-loop
        result = await formConsumer.save();
      } catch (err: any) {
        error = { ...err?.response?.data };
      }
    } else if (resultAction.action.name === 'delete_dlg') {
      try {
        // eslint-disable-next-line no-await-in-loop
        result = await formConsumer.delete();
      } catch (err: any) {
        error = { ...err.response.data };
      }
    }
    // propagate error to the next dialog
  } while (error && Object.keys(error).length);

  return result;
}
