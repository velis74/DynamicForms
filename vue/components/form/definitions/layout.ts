// eslint-disable-next-line max-classes-per-file
import FormField from './field';

let FormLayoutClass; // hoisting required: so we can use the class before it's even declared

function Column(layoutRow, def, fields) {
  const res = fields[def.field];
  let renderKey = 0;
  Object.defineProperty(res, 'layoutFieldComponentName', {
    get() { return 'FormField'; },
    enumerable: true,
    configurable: true,
  });
  Object.defineProperty(res, 'renderKey', {
    get() { return renderKey; },
    set(value) {
      renderKey = value;
      layoutRow.renderKey++;
    },
    enumerable: true,
  });
  return res;
}

class Group extends Column {
  public layoutFieldComponentName!: string;

  public title!: string;

  public layout!: typeof FormLayoutClass;

  constructor(layoutRow, def, fields) {
    super(layoutRow, def, fields);
    Object.defineProperty(this, 'layoutFieldComponentName', {
      get() { return 'FormFieldGroup'; },
      enumerable: true,
      configurable: true,
    });
    Object.defineProperty(this, 'title', { get() { return def.title; }, enumerable: true });
    Object.defineProperty(this, 'layout', { get() { return new FormLayoutClass(def.layout); }, enumerable: true });
    // footer=self.footer, title=self.title or sub_serializer.label,
    // uuid=sub_serializer.uuid,
    // layout=layout.as_component_def(sub_serializer, fields)
  }

  // eslint-disable-next-line class-methods-use-this
  get componentName() { return 'FormFieldGroup'; }
}

function FormColumn(layoutRow, columnDef, fields) {
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
  public renderKey!: number;

  constructor(rowDef, fields) {
    this.columns = rowDef.columns.map((column) => new FormColumn(this, column, fields));
    this.renderKey = 0;
    Object.defineProperty(this, 'componentName', { get() { return rowDef.component; }, enumerable: true });
  }

  get anyVisible() {
    return this.columns.reduce((result, column) => (result || column.isVisible), false);
  }
}

type FormLayoutFields = { [key: string]: FormField };

class FormLayout {
  public fields: FormLayoutFields;

  public rows: LayoutRow[];

  public componentName!: string;

  public fieldName!: string;

  constructor(layout) {
    this.fields = Object.keys(layout.fields).reduce((result: FormLayoutFields, fieldName: string) => {
      result[fieldName] = new FormField(layout.fields[fieldName]);
      return result;
    }, {});
    this.rows = layout.rows.map((row) => new LayoutRow(row, this.fields));
    Object.defineProperty(this, 'componentName', { get() { return layout.component_name; }, enumerable: true });
    // TODO field_name is not implemented yet on the backend
    Object.defineProperty(this, 'fieldName', { get() { return layout.field_name; }, enumerable: true });
  }
}

FormLayoutClass = FormLayout;

export default FormLayout;
