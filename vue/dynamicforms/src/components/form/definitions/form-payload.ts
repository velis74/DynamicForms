import _ from 'lodash';

import type { APIConsumer } from '../../api_consumer/namespace';
import DisplayMode from '../../classes/display-mode';

import type FormField from './field';
import type FormLayout from './layout';

export default class FormPayload {
  [key: string]: any;

  ['$extra-data']: any;

  constructor();
  constructor(data: FormPayload);
  constructor(data: APIConsumer.FormPayloadJSON, layout: FormLayout);
  constructor(data?: APIConsumer.FormPayloadJSON, layout?: FormLayout) {
    this.setData(data, layout);
  }

  addExtraData(data: { [key: string]: any }) {
    const extraData = { ...this['$extra-data'], ...data };
    Object.defineProperty(this, '$extra-data', { get() { return extraData; }, enumerable: false, configurable: true });
  }

  clear() {
    Object.getOwnPropertyNames(this).forEach((key) => {
      delete this[key];
    });
  }

  setData(data?: APIConsumer.FormPayloadJSON, layout?: FormLayout): FormPayload {
    let properties = {} as { [key: string]: any };
    let extraData = {};

    if (data == null) {
      // This is an empty constructor which creates just the class instance, without any payload nor any fields.
      // properties and extraData are already what they need to be
    } else if (data instanceof FormPayload) {
      [properties, extraData] = this.copyWithProperties(data);
    } else if (layout?.fields) {
      Object.values(layout.fields).forEach((field: FormField) => {
        if (field.visibility === DisplayMode.SUPPRESS) return;
        if (field.readOnly && !field.name.endsWith('-display')) {
          properties[field.name] = { get() { return data[field.name]; }, enumerable: false, configurable: true };
        } else {
          const self = this;
          self[field.name] = data[field.name];
          Object.defineProperty(self, `set${field.name}Value`, {
            get() { return function setValue(newValue: any) { self[field.name] = newValue; }; },
            enumerable: false,
            configurable: true,
          });
        }
      });
    }
    Object.defineProperty(this, '$extra-data', { get() { return extraData; }, enumerable: false, configurable: true });
    Object.defineProperties(this, properties);
    Object.defineProperty(this, '_properties', { get() { return properties; }, enumerable: false, configurable: true });

    return this;
  }

  replaceData(data?: APIConsumer.FormPayloadJSON, layout?: FormLayout): FormPayload {
    this.clear();
    return this.setData(data, layout);
  }

  private copyWithProperties(base: FormPayload): [_properties: any, extraData: any] {
    Object.entries(base).forEach(([itemName, itemValue]) => {
      this[itemName] = itemValue;
    });
    return [
      _.cloneDeep(base._properties), // eslint-disable-line no-underscore-dangle
      _.cloneDeep(base['$extra-data']),
    ];
  }
}
