namespace APIConsumer {
  import ActionsJSON = Actions.ActionsJSON;
  // type of primary keys. Django would normally have integers, but really, anything can be used as primary key
  import ErrorsJSON = Actions.ErrorsJSON;

  export type PKValueType = NonNullable<any>;

  export interface FormPayload {
    [key: string]: any;

    ['$extra-data']: any;

    addExtraData: (data: { [key: string]: any }) => void;
    deepClone: (base: FormPayload) => any[];
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
}
