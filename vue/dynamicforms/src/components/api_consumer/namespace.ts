// import FilteredActions from '../actions/filtered-actions';
// import TableColumns from '../table/definitions/columns';

import type { Actions } from '../actions/namespace';
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
    primary_key_name: string;
    titles: Titles;
  }

  export interface TableUXDefinition extends UXDefinition {
    columns: DfTable.ColumnJSON[];
    rows: DfTable.RowsData;
    ordering_parameter: string;
    ordering_style: unknown;
    responsive_table_layouts: DfTable.ResponsiveTableLayoutsDefinition;
    actions: Actions.ActionsJSON;
    filter: unknown;
    dialog: DfForm.FormLayoutJSON;
    record: unknown;
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
    actions: Actions.ActionsJSON,
    errors: Actions.ErrorsJSON,
  };

  export interface ConsumerLogicBaseInterface {
    pkName: string;
    setOrdering(parameter: string, style: any | null, counter: number): void;
    reload(filter: boolean): Promise<void>;
    deleteRow(tableRow: FormPayload): Promise<void>;
    dialogForm(pk: APIConsumer.PKValueType, formData: any, refresh: boolean): Promise<void>;
    title(which: 'table' | 'new' | 'edit'): string;
  }
  export interface ConsumerLogicAPIInterface extends ConsumerLogicBaseInterface {
    fetch(url: string, isTable: boolean, filter?: boolean): any;
  }
  export interface ConsumerLogicArrayInterface extends ConsumerLogicBaseInterface {}
}
