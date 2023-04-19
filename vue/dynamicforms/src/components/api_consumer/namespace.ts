// import FilteredActions from '../actions/filtered-actions';
// import TableColumns from '../table/definitions/columns';

namespace APIConsumer {
  import ActionsJSON = Actions.ActionsJSON;
  import ErrorsJSON = Actions.ErrorsJSON;

  // type of primary keys. Django would normally have integers, but really, anything can be used as primary key
  export type PKValueType = NonNullable<any>;

  export interface Titles {
    table: string;
    new: string;
    edit: string;
  }

  export interface UXDefinition {
    primary_key_name: string;
    titles: Titles;
  }

  export interface TableUXDefinition extends UXDefinition {
    columns: unknown
    rows: unknown
    ordering_parameter: unknown
    ordering_style: unknown
    responsive_table_layouts: unknown
    actions: unknown
    filter: unknown
    dialog: unknown
    record: unknown
  }

  export interface FormPayload {
    [key: string]: any;

    ['$extra-data']: any;

    addExtraData: (data: { [key: string]: any }) => void;
  }

  export interface FormLayoutType {
    componentName: string;
  }

  export type FormDefinition = {
    title: string,
    pkName: string,
    pkValue: PKValueType,
    layout: FormLayoutType,
    payload: FormPayload,
    loading: boolean,
    actions: ActionsJSON,
    errors: ErrorsJSON,
  };

  export interface ConsumerLogicBaseInterface {
    pkName: string;
    setOrdering(parameter: string, style: any | null, counter: number): void;
    reload(filter: boolean): Promise<void>;
    deleteRow(tableRow: FormPayload): Promise<void>;
    dialogForm(pk: APIConsumer.PKValueType, formData: any, refresh: boolean): Promise<void>;
    title(which: 'table' | 'new' | 'edit'): string;
  }
  export interface ConsumerLogicAPIInterface extends ConsumerLogicBaseInterface {}
  export interface ConsumerLogicArrayInterface extends ConsumerLogicBaseInterface {}
}
