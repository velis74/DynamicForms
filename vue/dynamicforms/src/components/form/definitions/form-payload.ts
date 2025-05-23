import { cloneDeep } from 'lodash-es';
import { reactive } from 'vue';

import type { APIConsumer } from '../../api_consumer/namespace';
import DisplayMode from '../../classes/display-mode';
import type { FormLayoutNS } from '../namespace';
import { FormLayoutTypeGuards } from '../namespace';

import type FormField from './field';
import type FormLayout from './layout';
import { Group } from './layout';

type FormLayoutInterface = FormLayoutNS.LayoutInterface;
type FormLayoutOrInterface = FormLayout | FormLayoutInterface;

function colIsGroup(col: any): col is Group {
  return col instanceof Group;
}

function collectAllFields(layout: FormLayoutOrInterface): FormField[] {
  const fields: FormField[] = [];
  if (layout.fields) {
    fields.push(...Object.values(layout.fields));
  }

  if (FormLayoutTypeGuards.isLayoutTemplate(layout)) {
    // Recursively check all nested groups that don't have their own nested objects
    layout.rows.forEach((row) => {
      row.columns?.forEach((col) => {
        if (FormLayoutTypeGuards.isGroupTemplate(col) && col.layout && col.field == null) {
          fields.push(...collectAllFields(col.layout));
        } else if (colIsGroup(col) && col.layout && col.field == null) {
          // TODO: this should not be. code too unpredictable. How the hell does col become group here?
          fields.push(...collectAllFields(col.layout));
        }
      });
    });
  }
  return fields;
}

export default class FormPayload {
  [key: string]: any;

  ['$extra-data']: any;

  private constructor(data?: APIConsumer.FormPayloadJSON, layout?: FormLayoutOrInterface) {
    this.setData(data, layout);
  }

  static create(): FormPayload;
  static create(data: FormPayload): FormPayload;
  static create(data: APIConsumer.FormPayloadJSON, layout?: FormLayoutOrInterface): FormPayload;
  static create(data?: APIConsumer.FormPayloadJSON, layout?: FormLayoutOrInterface): FormPayload {
    // Type assertion necessary to keep PyCharm from complaining about private functions
    return <FormPayload> reactive(new FormPayload(data, layout));
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

  setData(data?: APIConsumer.FormPayloadJSON, layout?: FormLayoutOrInterface): FormPayload {
    let properties = {} as { [key: string]: any };
    let extraData = {};

    if (data == null) {
      // This is an empty constructor which creates just the class instance, without any payload nor any fields.
      // properties and extraData are already what they need to be
    } else if (data instanceof FormPayload) {
      [properties, extraData] = this.copyWithProperties(data);
    } else if (layout?.fields) {
      collectAllFields(layout).forEach((field: FormField) => {
        if (field.visibility === DisplayMode.SUPPRESS) return;
        if (field.readOnly && field.name != null && !field.name.endsWith('-display')) {
          properties[field.name] = { get() { return data[field.name]; }, enumerable: false, configurable: true };
        } else if (field.name != null) {
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
      cloneDeep(base._properties), // eslint-disable-line no-underscore-dangle
      cloneDeep(base['$extra-data']),
    ];
  }
}
