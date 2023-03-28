import _ from 'lodash';

import DisplayMode from '../../classes/display-mode';

import FormField from './field';
import FormLayout from './layout';

import FormPayloadNS = APIConsumer.FormPayload;

export default class FormPayload implements FormPayloadNS {
  [key: string]: any;

  ['$extra-data']: any;

  constructor();
  constructor(data: FormPayload);
  constructor(data: Record<string, any>, layout: FormLayout);
  constructor(data?: Record<string, any>, layout?: FormLayout) {
    let properties = {} as { [key: string]: any };
    let extraData = {};

    if (data == null) {
      // This is an empty constructor which creates just the class instance, without any payload nor any fields.
      // properties and extraData are already what they need to be
    } else if (data instanceof FormPayload) {
      [properties, extraData] = this.deepClone(data);
    } else if (layout?.fields) {
      Object.values(layout.fields).forEach((field: FormField) => {
        if (field.visibility === DisplayMode.SUPPRESS) return;
        if (field.readOnly) {
          properties[field.name] = { get() { return data[field.name]; }, enumerable: false };
        } else {
          const self = this;
          self[field.name] = data[field.name];
          Object.defineProperty(self, `set${field.name}Value`, {
            get() { return function setValue(newValue: any) { self[field.name] = newValue; }; },
            enumerable: false,
          });
        }
      });
    }
    Object.defineProperty(this, '$extra-data', { get() { return extraData; }, enumerable: false, configurable: true });
    Object.defineProperties(this, properties);
    Object.defineProperty(this, '_properties', { get() { return properties; }, enumerable: false });
  }

  addExtraData(data: { [key: string]: any }) {
    const extraData = { ...this['$extra-data'], ...data };
    Object.defineProperty(this, '$extra-data', { get() { return extraData; }, enumerable: false, configurable: true });
  }

  deepClone(base: FormPayload) {
    Object.entries(base).forEach(([itemName, itemValue]) => {
      this[itemName] = itemValue;
    });
    return [
      _.cloneDeep(base._properties), // eslint-disable-line no-underscore-dangle
      _.cloneDeep(base['$extra-data']),
    ];
  }
}
