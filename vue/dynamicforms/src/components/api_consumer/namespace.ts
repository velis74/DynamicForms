// import FilteredActions from '../actions/filtered-actions';
// import TableColumns from '../table/definitions/columns';

import { Ref } from 'vue';

import { IHandlers } from '../actions/action-handler-composable';
import type FilteredActions from '../actions/filtered-actions';
import type { ActionsNS } from '../actions/namespace';
import type FormPayload from '../form/definitions/form-payload';
import type FormLayout from '../form/definitions/layout';
import type { DfForm } from '../form/namespace';
import type { DfTable } from '../table/namespace';

export namespace APIConsumer {
  // type of primary keys. Django would normally have integers, but really, anything can be used as primary key
  export type PKValueType = NonNullable<any>;

  export interface Titles {
    table: string;
    new: string;
    edit: string;
  }

  export interface UXDefinition {
    primary_key_name: string
    titles: Titles
    dialog: DfForm.FormLayoutJSON
    actions: ActionsNS.ActionsJSON
    record: FormPayloadJSON
  }

  export interface TableUXDefinition extends UXDefinition {
    columns: DfTable.ColumnJSON[];
    rows: DfTable.RowsData;
    ordering_parameter: string;
    ordering_style: unknown;
    responsive_table_layouts: DfTable.ResponsiveTableLayoutsDefinition;
    filter: unknown;
    record: FormPayloadJSON;
  }

  export interface FormUXDefinition extends UXDefinition {
    record: FormPayloadJSON
  }

  export type FormPayloadJSON = { [key: string]: any; } | null;

  export type FormDefinition = {
    title: string,
    pkName: string,
    pkValue: PKValueType,
    layout: FormLayout,
    payload: FormPayload,
    loading: boolean,
    actions: FilteredActions,
    actionHandlers?: IHandlers,
    errors: ActionsNS.ErrorsJSON,
  };

  export interface ConsumerLogicBaseInterface {
    updateCounter: Ref<number>;
    pkName: string;
    setDialogHandlers(handlers?: IHandlers): void;
    setOrdering(parameter: string, style: any | null, counter: number): void;
    reload(filter: boolean): Promise<void>;
    deleteRow(tableRow: FormPayload): Promise<void>;
    dialogForm(pk: APIConsumer.PKValueType): Promise<any>;
    title(which: 'table' | 'new' | 'edit'): string;
    tableDefinition: Record<string, unknown>; // TODO: this needs to be changed to what is actually returned
    formDefinition: APIConsumer.FormDefinition;
    filter(filterData: Object | null): Promise<void>;
    reload(filter?: boolean): Promise<void>;
  }
  export interface ConsumerLogicAPIInterface extends ConsumerLogicBaseInterface {
    fetch(): any;
    fetchNewRows(url: string): any;
  }
  export interface ConsumerLogicArrayInterface extends ConsumerLogicBaseInterface {}
}
