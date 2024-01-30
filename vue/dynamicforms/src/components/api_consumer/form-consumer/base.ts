import { IHandlers } from '../../actions/action-handler-composable';
import FilteredActions from '../../actions/filtered-actions';
import { PrimaryKeyType } from '../../adapters/api/namespace';
import { FormAdapter } from '../../adapters/namespace';
import FormPayload from '../../form/definitions/form-payload';
import FormLayout from '../../form/definitions/layout';
import dfModal from '../../modal/modal-view-api';
import { gettext } from '../../util/translations-mixin';
import { APIConsumer } from '../namespace';

import { FormConsumerHooks, FormExecuteResult } from './namespace';

export default abstract class FormConsumerBase<T = any> {
  pkName: keyof T & string = <keyof T & string> 'id';

  ux_def: APIConsumer.FormUXDefinition = {} as APIConsumer.FormUXDefinition;

  layout: FormLayout | null = null;

  titles: APIConsumer.Titles = { new: '', edit: '', table: '' };

  actions: FilteredActions = new FilteredActions({});

  data?: FormPayload;

  loading: boolean = false;

  errors: any = {};

  actionHandlers?: IHandlers;

  protected api!: FormAdapter<T>;

  beforeDialog?: (instance: any) => void;

  afterDialog?: (instance: any, action: any) => void;

  protected constructor(handlers?: IHandlers, hooks?: FormConsumerHooks<FormConsumerBase>) {
    this.actionHandlers = handlers;
    Object.assign(this, hooks);
  }

  title(which: 'table' | 'new' | 'edit'): string {
    /**
     * @return Name of the form for the action we call.
     */
    return this.titles[which] ?? '';
  }

  get pkValue(): PrimaryKeyType {
    return this.data?.[this.pkName] ?? 'new';
  }

  get definition(): APIConsumer.FormDefinition {
    this.layout = new FormLayout(this.ux_def.dialog);
    this.data = this.data ?
      this.data.replaceData(this.ux_def.record, this.layout) : FormPayload.create(this.ux_def.record, this.layout);
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

  delete = async (): Promise<T> => {
    if (this.pkValue !== undefined && this.pkValue !== 'new') return this.api.delete();
    // eslint-disable-next-line @typescript-eslint/no-throw-literal
    throw ({ response: { data: { detail: gettext('Cannot delete new record.') } } });
  };

  save = async (): Promise<T> => {
    if (this.pkValue !== 'new' && !!this.pkValue) return this.api.update(<T> this.data);
    return this.api.create(<T> this.data);
  };

  getRecord = async (): Promise<APIConsumer.FormPayloadJSON> => this.api.retrieve() as APIConsumer.FormPayloadJSON;

  getUXDefinition = async () => {
    if (!this.layout) {
      this.ux_def = await this.api.componentDefinition();
      this.pkName = <keyof T & string> this.ux_def.primary_key_name;
      this.titles = this.ux_def.titles;
    } else {
      this.ux_def.record = await this.getRecord();
    }

    return this.definition;
  };
}
