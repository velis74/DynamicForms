// eslint-disable-next-line max-classes-per-file
import DisplayMode from '../../classes/display-mode';
import DialogSize from '../../modal/definitions/dialog-size';
import { DfForm } from '../namespace';

import FormField from './field';

let FormLayoutClass: typeof FormLayout; // hoisting required: so we can use the class before it's even declared

export class Column extends FormField {
  layoutFieldComponentName!: string;

  constructor(layoutRow: LayoutRow, def: DfForm.FormFieldJSON) {
    super(def);
    let renderKey = 0;
    Object.defineProperty(this, 'layoutFieldComponentName', {
      get() { return 'FormField'; },
      enumerable: true,
      configurable: true,
    });
    Object.defineProperty(this, 'renderKey', {
      get() { return renderKey; },
      set(value) {
        renderKey = value;
        layoutRow.renderKey++;
      },
      enumerable: true,
    });
  }
}

export class Group extends Column {
  public title!: string;

  public layout!: FormLayout;

  constructor(layoutRow: LayoutRow, def: DfForm.FormLayoutRowsColumnJSON, fieldDef: DfForm.FormFieldJSON) {
    if (fieldDef == null) {
      const fd: DfForm.FormFieldJSON = {
        uuid: crypto.randomUUID(),
        name: null,
        label: '',
        placeholder: '',
        alignment: 'left',
        visibility: { form: DisplayMode.FULL, table: DisplayMode.SUPPRESS },
        render_params: {
          input_type: '',
          form_component_name: 'df-form-layout',
        },
        read_only: true,
        choices: [],
        width_classes: '',
        help_text: '',
        allow_null: false,
      };
      super(layoutRow, fd);
    } else {
      super(layoutRow, fieldDef);
    }
    Object.defineProperty(this, 'layoutFieldComponentName', {
      get() { return 'FormFieldGroup'; },
      enumerable: true,
      configurable: true,
    });
    Object.defineProperty(this, 'title', { get() { return def.title; }, enumerable: true });
    Object.defineProperty(
      this,
      'layout',
      { get() { return new FormLayoutClass(def.layout as DfForm.FormLayoutJSON); }, enumerable: true },
    );
    Object.defineProperty(
      this,
      'componentName',
      { get() { return 'FormFieldGroup'; }, enumerable: true, configurable: true },
    );
    // footer=self.footer, title=self.title or sub_serializer.label,
    // uuid=sub_serializer.uuid,
    // layout=layout.as_component_def(sub_serializer, fields)
  }
}

function FormColumn(layoutRow: LayoutRow, columnDef: DfForm.FormLayoutRowsColumnJSON, fieldDef: DfForm.FormFieldJSON) {
  switch (columnDef.type) {
  case 'column':
    return new Column(layoutRow, fieldDef);
  case 'group':
    return new Group(layoutRow, columnDef, fieldDef);
  default:
    throw Error(`Unknown layout column type "${columnDef.type}"`);
  }
}

type FormLayoutFields = { [key: string]: FormField };

class LayoutRow {
  public renderKey!: number;

  public columns: Column[];

  public componentName!: string;

  constructor(
    rowDef: DfForm.FormLayoutRowJSON,
    fields: FormLayoutFields,
    fieldDefs: DfForm.FormLayoutFieldsCollection,
  ) {
    this.columns = rowDef.columns.map((column) => {
      const res = FormColumn(this, column, fieldDefs[column.field]);
      fields[column.field] = res;
      return res;
    });
    this.renderKey = 0;
    Object.defineProperty(this, 'componentName', { get() { return rowDef.component; }, enumerable: true });
  }

  get anyVisible() {
    return this.columns.reduce((result, column) => (result || column.isVisible), false);
  }
}

class FormLayout {
  public fields: FormLayoutFields;

  public rows: LayoutRow[];

  public componentName!: string;

  public fieldName!: string;

  public size!: DialogSize;

  constructor(layout?: DfForm.FormLayoutJSON) {
    if (layout === undefined) {
      this.fields = {};
      this.rows = [];
      Object.defineProperty(this, 'size', { get() { return DialogSize.DEFAULT; }, enumerable: true });
    } else {
      this.fields = {};
      this.rows = layout.rows.map((row) => new LayoutRow(row, this.fields, layout.fields));
      Object.keys(layout.fields).forEach((fieldName: string) => {
        // here we generically add all the fields that were not listed in the layout definition
        if (!(fieldName in this.fields)) this.fields[fieldName] = new FormField(layout.fields[fieldName]);
      });
      Object.defineProperty(this, 'componentName', { get() { return layout.component_name; }, enumerable: true });
      // TODO field_name is not implemented yet on the backend
      Object.defineProperty(this, 'fieldName', { get() { return layout.field_name; }, enumerable: true });
      Object.defineProperty(this, 'size', { get() { return DialogSize.fromString(layout.size); }, enumerable: true });
    }
  }
}

FormLayoutClass = FormLayout;

export default FormLayout;
