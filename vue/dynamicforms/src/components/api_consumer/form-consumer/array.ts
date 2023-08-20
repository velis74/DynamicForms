import { IHandlers } from '../../actions/action-handler-composable';
import FormPayload from '../../form/definitions/form-payload';
import dfModal from '../../modal/modal-view-api';
import { APIConsumer } from '../namespace';

import FormConsumerBase from './base';
import type { FormConsumerHooks, FormExecuteResult } from './namespace';

export default class FormConsumerArray<T = any> extends FormConsumerBase {
  declare beforeDialog?: (instance: FormConsumerArray) => void;

  declare afterDialog?: (instance: FormConsumerArray, action: any) => void;

  constructor(
    UXDefinition: APIConsumer.FormUXDefinition,
    actionHandlers?: IHandlers,
    hooks?: FormConsumerHooks<FormConsumerArray>,
  ) {
    super();

    this.ux_def = UXDefinition;
    this.actionHandlers = actionHandlers;

    Object.assign(this, hooks);
  }

  getRecord = (): APIConsumer.FormPayloadJSON => this.data ?? null;

  getUXDefinition = () => {
    if (!this.layout) {
      this.pkName = this.ux_def.primary_key_name;
      this.titles = this.ux_def.titles;
    }
    this.ux_def.record = this.getRecord();

    return this.definition;
  };

  execute = async (data: Partial<T> | null): Promise<FormExecuteResult> => {
    const definition = this.definition;

    Object.assign(this.data!, data);

    this.beforeDialog?.(this);

    const resultAction = await dfModal.fromFormDefinition(definition);

    this.afterDialog?.(this, resultAction);

    return {
      data: this.data!,
      action: resultAction,
    };
  };

  async delete(): Promise<FormPayload | undefined> { return this.data; }

  async save(): Promise<FormPayload | undefined> { return this.data; }
}
