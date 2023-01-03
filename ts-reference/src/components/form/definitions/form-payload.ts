import _ from 'lodash';

import ColumnDisplay from '@/components/classes/display-mode';

interface FormPayload {
  get _properties(): Function;
}

class FormPayload {

  constructor(data: any, layout: any) {
    const properties: any = {};
    Object.values(layout.fields).forEach((field: any) => {
      if (field.visibility === ColumnDisplay.SUPPRESS) return;
      if (field.readOnly) {
        properties[field.name] = { get() { return data[field.name]; }, enumerable: false };
      } else {
        this[field.name] = data[field.name];
        Object.defineProperty(this, `set${field.name}Value`, {
          get() { return function setValue(newValue: any) { this[field.name] = newValue; }; },
          enumerable: false,
        });
      }
    });
    Object.defineProperties(this, properties);
    Object.defineProperty(this, '_properties', { get() { return properties; }, enumerable: false });
  }

  deepClone() {
    const res: FormPayload = _.cloneDeep(this);
    Object.defineProperties(res, this._properties);
    return res;
  }
}

export default FormPayload;
