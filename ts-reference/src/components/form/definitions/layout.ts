import FormField from '@/components/form/definitions/field';

// eslint-disable-next-line prefer-const
let FormLayoutClass: any; // hoisting required: so we can use the class before it's even declared

// TODO: Je tole prav prepisano?
class Column {
  renderKey: number = 0

  constructor(layoutRow: any, def: any, fields: any) {
    const res = fields[def.field];
    this.renderKey = 0
    Object.keys(res).forEach(key => {
      Object.defineProperty(this, key, { get() { return res[key]; }, enumerable: true })
    })
    Object.defineProperty(this, 'layoutFieldComponentName', { get() { return 'FormField'; }, enumerable: true });
    Object.defineProperty(this, 'renderKey', {
      get() { return this.renderKey; },
      set(value) {
        this.renderKey = value;
        layoutRow.renderKey++;
      },
      enumerable: true,
    });
  }
}

class Group extends Column {
  constructor(layoutRow: any, def: any, fields: any) {
    super(layoutRow, def, fields);
    Object.defineProperty(this, 'title', { get() { return def.title; }, enumerable: true });
    Object.defineProperty(this, 'layout', { get() { return new FormLayoutClass(def.layout); }, enumerable: true });
    // footer=self.footer, title=self.title or sub_serializer.label,
    // uuid=sub_serializer.uuid,
    // layout=layout.as_component_def(sub_serializer, fields)
  }

  // eslint-disable-next-line class-methods-use-this
  get componentName() { return 'FormFieldGroup'; }
}

function FormColumn(layoutRow: any, columnDef: any, fields: any) {
  switch (columnDef.type) {
  case 'column':
    return new Column(layoutRow, columnDef, fields);
  case 'group':
    return new Group(layoutRow, columnDef, fields);
  default:
    throw Error(`Unknown layout column type "${columnDef.type}"`);
  }
}

class LayoutRow {
  private columns: any;
  private renderKey: number;

  constructor(rowDef: any, fields: any) {
    this.columns = rowDef.columns.map((column: any) => FormColumn(this, column, fields));
    this.renderKey = 0;
    Object.defineProperty(this, 'componentName', { get() { return rowDef.component; }, enumerable: true });
  }

  get anyVisible() {
    return this.columns.reduce((result: any, column: any) => (result || column.isVisible), false);
  }
}

class FormLayout {
  fields: {};
  private rows: any;

  constructor(layout: any) {
    this.fields = Object.keys(layout.fields).reduce((result: any, fieldName) => {
      result[fieldName] = new FormField(layout.fields[fieldName]);
      return result;
    }, {});
    this.rows = layout.rows.map((row: any) => new LayoutRow(row, this.fields));
    Object.defineProperty(this, 'componentName', { get() { return layout.component_name; }, enumerable: true });
    // TODO field_name is not implemented yet on the backend
    Object.defineProperty(this, 'fieldName', { get() { return layout.field_name; }, enumerable: true });
  }
}

FormLayoutClass = FormLayout;

export default FormLayout;
