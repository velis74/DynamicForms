import ColumnDisplay from '../../classes/display_mode';

export default class FormPayload {
  constructor(data, layout) {
    Object.values(layout.fields).forEach((field) => {
      if (field.visibility === ColumnDisplay.SUPPRESS) return;
      if (field.readOnly) {
        Object.defineProperty(this, field.name, { get() { return data[field.name]; }, enumerable: false });
      } else {
        this[field.name] = data[field.name];
        Object.defineProperty(this, `set${field.name}Value`, {
          get() { return function setValue(newValue) { this[field.name] = newValue; }; },
          enumerable: false,
        });
      }
    });
  }
}
