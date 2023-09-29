import { IHandlers } from '../../actions/action-handler-composable';
import FilteredActions from '../../actions/filtered-actions';
import { PrimaryKeyType } from '../../api_view/namespace';
import FormPayload from '../../form/definitions/form-payload';
import FormLayout from '../../form/definitions/layout';
import dfModal from '../../modal/modal-view-api';
import { APIConsumer } from '../namespace';

import { FormExecuteResult } from './namespace';

export default abstract class FormConsumerBase<T = any> {
  pkName: string = 'id';

  ux_def: APIConsumer.FormUXDefinition = {} as APIConsumer.FormUXDefinition;

  layout: FormLayout | null = null;

  titles: APIConsumer.Titles = { new: '', edit: '', table: '' };

  actions: FilteredActions = new FilteredActions({});

  data?: FormPayload;

  loading: boolean = false;

  errors: any = {};

  actionHandlers?: IHandlers;

  beforeDialog?: (instance: any) => void;

  afterDialog?: (instance: any, action: any) => void;

  title(which: 'table' | 'new' | 'edit'): string {
    /**
     * @return Name of the form for the action we call.
     */
    return this.titles[which] ?? '';
  }

  get pkValue(): PrimaryKeyType {
    return this.data?.[this.pkName];
  }

  get definition(): APIConsumer.FormDefinition {
    this.layout = new FormLayout(this.ux_def.dialog);
    this.data = new FormPayload(this.ux_def.record, this.layout);
    this.actions = new FilteredActions(this.ux_def.actions);
    return {
      title: this.title(this.pkValue === 'new' ? 'new' : 'edit'),
      pkName: this.pkName,
      pkValue: this.pkValue,
      layout: this.layout,
      payload: this.data,
      loading: this.loading,
      actions: this.actions,
      errors: this.errors,
      actionHandlers: this.actionHandlers,
    };
  }

  withErrors = (errors: any) => {
    this.errors = errors;
    return this;
  };

  execute = async (defaultData?: Partial<T> | null): Promise<FormExecuteResult<T>> => {
    const definition = await this.getUXDefinition();
    if (defaultData) {
      Object.assign(definition.payload, defaultData);
      this.data = definition.payload;
    }

    this.beforeDialog?.(this);

    const resultAction = await dfModal.fromFormDefinition(definition);

    this.afterDialog?.(this, resultAction);

    return {
      data: <Partial<T>> <unknown> this.data!,
      action: resultAction,
    };
  };

  abstract delete(): Promise<T | undefined>;

  abstract save(): Promise<T>;

  abstract getRecord: () => APIConsumer.FormPayloadJSON | Promise<APIConsumer.FormPayloadJSON>;

  abstract getUXDefinition: () => APIConsumer.FormDefinition | Promise<APIConsumer.FormDefinition>;
}
