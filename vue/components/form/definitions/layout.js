// eslint-disable-next-line max-classes-per-file
import FormField from './field';

let FormLayoutClass; // hoisting required: so we can use the class before it's even declared

function Column(def, fields) {
  const res = fields[def.field];
  Object.defineProperty(res, 'layoutFieldComponentName', { get() { return 'FormField'; }, enumerable: true });
  return res;
}

class Group extends Column {
  constructor(def, fields) {
    super(def, fields);
    Object.defineProperty(this, 'title', { get() { return def.title; }, enumerable: true });
    Object.defineProperty(this, 'layout', { get() { return new FormLayoutClass(def.layout); }, enumerable: true });
    // footer=self.footer, title=self.title or sub_serializer.label,
    // uuid=sub_serializer.uuid,
    // layout=layout.as_component_def(sub_serializer, fields)
  }

  // eslint-disable-next-line class-methods-use-this
  get componentName() { return 'FormFieldGroup'; }
}

function FormColumn(columnDef, fields) {
  switch (columnDef.type) {
  case 'column':
    return new Column(columnDef, fields);
  case 'group':
    return new Group(columnDef, fields);
  default:
    throw Error(`Unknown layout column type "${columnDef.type}"`);
  }
}

class LayoutRow {
  constructor(rowDef, fields) {
    this.columns = rowDef.columns.map((column) => new FormColumn(column, fields));
    Object.defineProperty(this, 'componentName', { get() { return rowDef.component; }, enumerable: true });
  }

  get anyVisible() {
    return this.columns.reduce((result, column) => (result || column.isVisible), false);
  }
}

class FormLayout {
  constructor(layout) {
    this.fields = Object.keys(layout.fields).reduce((result, fieldName) => {
      result[fieldName] = new FormField(layout.fields[fieldName]);
      return result;
    }, {});
    this.rows = layout.rows.map((row) => new LayoutRow(row, this.fields));
    Object.defineProperty(this, 'componentName', { get() { return layout.component_name; }, enumerable: true });
  }
}

FormLayoutClass = FormLayout;

export default FormLayout;
