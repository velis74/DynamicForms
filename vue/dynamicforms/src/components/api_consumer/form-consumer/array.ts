import { UnwrapNestedRefs } from 'vue';

import { IHandlers } from '../../actions/action-handler-composable';
import createInternalRecord from '../../util/InternalRecord';
import { APIConsumer } from '../namespace';

import FormConsumerBase from './base';
import type { FormConsumerHooks } from './namespace';

let counter = 0;

export interface InMemoryParams {
  definition: APIConsumer.FormUXDefinition,
  data: UnwrapNestedRefs<any[]>,
}

export default class FormConsumerArray<T = any> extends FormConsumerBase<T> {
  declare beforeDialog?: (instance: FormConsumerArray) => void;

  declare afterDialog?: (instance: FormConsumerArray, action: any) => void;

  private readonly internalData: UnwrapNestedRefs<any[]>;

  constructor(
    params: InMemoryParams,
    actionHandlers?: IHandlers,
    hooks?: FormConsumerHooks<FormConsumerArray>,
  ) {
    super();

    this.ux_def = params.definition;
    this.internalData = params.data;
    this.actionHandlers = actionHandlers;

    Object.assign(this, hooks);
  }

  getRecord = (): APIConsumer.FormPayloadJSON => this.data ?? null;

  getInternalRecord = (pk: APIConsumer.PKValueType) => (
    this.internalData.find((element: any) => (element[this.pkName] === pk))
  );

  getUXDefinition = () => {
    if (!this.layout) {
      this.pkName = this.ux_def.primary_key_name;
      this.titles = this.ux_def.titles;
    }
    this.ux_def.record = this.getRecord();

    return this.definition;
  };

  delete = async (): Promise<T | undefined> => {
    const recordIdx = this.internalData.findIndex((element) => element[this.pkName] === this.pkValue);
    this.internalData.splice(recordIdx, 1);
    return this.data as T | undefined;
  };

  save = async (): Promise<T> => {
    if (this.pkValue !== 'new' && this.pkValue) {
      // we are updating a record
      const record = this.getInternalRecord(this.pkValue);
      for (const [key, value] of Object.entries(this.data as any)) {
        record[key] = value;
      }
    } else {
      // create new record
      this.internalData.push(createInternalRecord({ ...this.data }, this.pkName, --counter));
    }

    return this.data as T;
  };
}
