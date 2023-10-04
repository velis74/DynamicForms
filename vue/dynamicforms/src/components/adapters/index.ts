import { min } from 'lodash';
import { MaybeRef, ref, Ref } from 'vue';

import { APIConsumer } from '../api_consumer/namespace';
import createInternalRecord from '../util/internal-record';

import { PrimaryKeyBaseType } from './api/namespace';
import { FormAdapter } from './namespace';

interface InMemoryParams<T> {
  definition: APIConsumer.FormUXDefinition,
  data: T[],
  pk: MaybeRef<PrimaryKeyBaseType>
  pkName: keyof T & string,
  record: T,
}

class InMemoryImplementation<T extends object = any> implements FormAdapter<T> {
  data: T[];

  record: T;

  ux_def: APIConsumer.FormUXDefinition;

  pk: Ref<PrimaryKeyBaseType>;

  pkName: keyof T & string;

  counter: number;

  constructor(params: InMemoryParams<T>) {
    this.data = params.data;
    this.ux_def = params.definition;
    this.pk = ref(params.pk);
    this.pkName = params.pkName;
    this.record = params.record;

    this.counter = 0;
  }

  private comparePk(element: any) {
    return element[this.pkName] === this.pk.value;
  }

  componentDefinition = () => this.ux_def;

  retrieve = () => this.data.find((element) => this.comparePk(element))!;

  create(data: T): T {
    const lowestIndex = min([min(this.data.map((element) => element[this.pkName] as PrimaryKeyBaseType)), 0]);
    this.data.push(createInternalRecord({ ...data }, this.pkName, (lowestIndex ?? 0) - 1));
    return data;
  }

  async update(data: T): Promise<T> {
    const record = this.retrieve();
    for (const [key, value] of Object.entries(data)) {
      record[key as keyof T] = value;
    }
    this.data.push(record);
    return record;
  }

  delete() {
    const recordIdx = this.data.findIndex((element) => this.comparePk(element));
    const record = this.data[recordIdx];
    this.data.splice(recordIdx, 1);
    return record;
  }
}

export default InMemoryImplementation;
