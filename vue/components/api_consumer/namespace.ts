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

  export interface LogicInterface {
    // private baseURL: string;
    pkName: string;
    // private fields: { [key: string]: { [key: string]: any } };
    // private tableColumns: TableColumns[];
    // private loading: boolean;
    // private responsiveTableLayouts: null;
    // private formFields: { [key: string]: unknown };
    // private formLayout: FormLayoutType;
    // private formComponent: string; // component responsible for rendering the form layout
    // private errors: { [key: string]: unknown };
    // private actions: FilteredActions;
    // private ux_def: Object;
    // private rows: unknown[];
    // private formData: FormDataType;
    // private requestedPKValue: null;
    // private ordering: { parameter: string, style: null, counter: number };
    // private filterDefinition: null;
    // private filterData: Object;
    fetch: (url: string, isTable: boolean, filter?: boolean) => any;
  }
}
