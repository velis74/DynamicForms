import { Ref } from 'vue';

import { IHandlers } from '../../actions/action-handler-composable';
import DetailViewApi from '../../api_view/detail-view-api';
import { PrimaryKeyType } from '../../api_view/namespace';
import dfModal from '../../modal/modal-view-api';
import type { APIConsumer } from '../namespace';

import FormConsumerBase from './base';
import type { FormConsumerHook, FormConsumerHooks, FormExecuteResult } from './namespace';

class FormConsumerApi<T = any> extends FormConsumerBase {
  readonly api: DetailViewApi<T>;

  declare beforeDialog?: FormConsumerHook;

  declare afterDialog?: (instance: FormConsumerApi, action: any) => void;

  constructor(
    baseUrl: string | Ref<string>,
    trailingSlash: boolean = false,
    pk?: PrimaryKeyType,
    actionHandlers?: IHandlers,
    hooks?: FormConsumerHooks<FormConsumerApi>,
  ) {
    super();

    this.api = new DetailViewApi<T>(baseUrl, trailingSlash, pk);
    this.actionHandlers = actionHandlers;

    Object.assign(this, hooks);
  }

  getRecord = async (): Promise<APIConsumer.FormPayloadJSON> => (
    await this.api.retrieve() as APIConsumer.FormPayloadJSON
  );

  getUXDefinition = async (): Promise<APIConsumer.FormDefinition> => {
    if (!this.layout) {
      this.ux_def = await this.api.componentDefinition();
      this.pkName = this.ux_def.primary_key_name;
      this.titles = this.ux_def.titles;
    } else {
      this.ux_def.record = await this.getRecord();
    }

    return this.definition;
  };

  delete = async (): Promise<T | undefined> => this.api.delete();

  save = async () => {
    if (this.pkValue && this.pkValue !== 'new') return this.api.update(<T> this.data);
    return this.api.create(<T> this.data);
  };

  execute = async (defaultData?: Partial<T> | null): Promise<FormExecuteResult> => {
    const definition = await this.getUXDefinition();
    if (defaultData) {
      Object.assign(definition.payload, defaultData);
      this.data = definition.payload;
    }

    this.beforeDialog?.(this);

    const resultAction = await dfModal.fromFormDefinition(definition);

    this.afterDialog?.(this, resultAction);

    return {
      data: this.data!,
      action: resultAction,
    };
  };
}

export default FormConsumerApi;
