import _ from 'lodash';

import ColumnDisplay from '../../classes/display_mode';

export default class FormPayload {
  constructor(data, layout) {
    const properties = {};

    Object.values(layout.fields).forEach((field) => {
      if (field.visibility === ColumnDisplay.SUPPRESS) return;
      if (field.readOnly) {
        properties[field.name] = { get() { return data[field.name]; }, enumerable: false };
      } else {
        this[field.name] = data[field.name];
        Object.defineProperty(this, `set${field.name}Value`, {
          get() { return function setValue(newValue) { this[field.name] = newValue; }; },
          enumerable: false,
        });
      }
    });
    Object.defineProperties(this, properties);
    Object.defineProperty(this, '_properties', { get() { return properties; }, enumerable: false });
  }

  deepClone() {
    const res = _.cloneDeep(this);
    Object.defineProperties(res, this._properties);
    return res;
  }
}
