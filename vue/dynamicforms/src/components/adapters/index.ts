import { computed, ComputedRef, MaybeRef, ref, Ref } from 'vue';

import { APIConsumer } from '../api_consumer/namespace';
import createInternalRecord, { isInternalRecord } from '../util/internal-record';

import { PrimaryKeyBaseType } from './api/namespace';
import { FormAdapter } from './namespace';

export * from './api';

interface InMemoryParams<T> {
  definition: APIConsumer.FormUXDefinition,
  data: T[],
  pk: MaybeRef<PrimaryKeyBaseType>
  pkName: keyof T & string,
}

class InMemoryImplementation<T extends object = any> implements FormAdapter<T> {
  data: T[];

  ux_def: APIConsumer.FormUXDefinition;

  pk: Ref<PrimaryKeyBaseType>;

  pkName: keyof T & string;

  counter: ComputedRef<number>;

  constructor(params: InMemoryParams<T>) {
    this.data = params.data;
    this.ux_def = params.definition;
    this.pk = ref(params.pk);
    this.pkName = params.pkName;

    this.counter = computed(() => -this.data.filter((element) => isInternalRecord(element)).length);
  }

  private comparePk(element: any) {
    return element[this.pkName] === this.pk.value;
  }

  componentDefinition = () => this.ux_def;

  retrieve = () => this.data.find((element) => this.comparePk(element))!;

  create(data: T): T {
    this.data.push(createInternalRecord({ ...data }, this.pkName, this.counter.value - 1));
    return data;
  }

  async update(data: T): Promise<T> {
    const record = this.retrieve();
    for (const [key, value] of Object.entries(data)) {
      record[key as keyof T] = value;
    }
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
