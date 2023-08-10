import { IHandlers } from '../../actions/action-handler-composable';
import FilteredActions from '../../actions/filtered-actions';
import FormPayload from '../../form/definitions/form-payload';
import FormLayout from '../../form/definitions/layout';
import { APIConsumer } from '../namespace';

export default abstract class FormConsumerBase {
  requestedPKValue?: APIConsumer.PKValueType;

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

  get pkValue() {
    return this.data?.[this.pkName] ?? this.requestedPKValue;
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

  abstract getRecord: () => APIConsumer.FormPayloadJSON | Promise<APIConsumer.FormPayloadJSON>;

  abstract getUXDefinition: () => APIConsumer.FormDefinition | Promise<APIConsumer.FormDefinition>;
}
