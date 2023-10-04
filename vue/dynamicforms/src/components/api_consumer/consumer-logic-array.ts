import { nextTick } from 'vue';

import FormPayload from '../form/definitions/form-payload';
import { TransformationFunctionBase } from '../table/definitions/column-ordering';
import OrderingDirection from '../table/definitions/column-ordering-direction';
import TableRows from '../table/definitions/rows';
import getObjectFromPath from '../util/get-object-from-path';
import { toExternalRecordCopy } from '../util/internal-record';

import ConsumerLogicBase from './consumer-logic-base';
import FormConsumerOneShotArray from './form-consumer/one-shot/array';
import { APIConsumer } from './namespace';

class ConsumerLogicArray extends ConsumerLogicBase implements APIConsumer.ConsumerLogicArrayInterface {
  private readonly records: any[];

  constructor(UXDefinition: APIConsumer.TableUXDefinition, records: any[]) {
    super();

    this.ux_def = UXDefinition;
    this.records = records;

    this.processUXDefinition(this.ux_def);
  }

  get internalRecords() { return this.records.map(toExternalRecordCopy); }

  order(): any[] {
    /**
     * Order internal records according to filters
     */
    const orderingTransformationFunction = this.ordering ?
      getObjectFromPath(<string> this.ordering.style) as TransformationFunctionBase :
      undefined;
    const orderingValue = this.tableColumns[0].ordering.calculateOrderingFunction(orderingTransformationFunction);
    // ordering can be an empty object
    if (orderingValue?.length) {
      // extract values
      const columnName = orderingValue[0].name;
      const direction = orderingValue[0].direction === OrderingDirection.ASC;

      // For clearer syntax, function can be easily rewritten here to be more readable
      const orderingFunction = (val1: any, val2: any): number => (
        // eslint-disable-next-line no-nested-ternary
        val1[columnName] === val2[columnName] ? 0 : (
          (direction ? val1[columnName] > val2[columnName] : val1[columnName] < val2[columnName]) ?
            1 : -1
        )
      );

      return this.internalRecords.sort(orderingFunction);
    }
    return this.internalRecords;
  }

  async reload(filter: boolean = false): Promise<void> {
    /**
     * Reload internal records from external records, filter and order them
     */
    await nextTick(); // due to vue's reactivity

    // TODO: do filtering
    if (filter) {
      throw new Error('Not implemented');
    }
    const res = this.order();
    this.rows = new TableRows(this, res);
  }

  async getFormDefinition(pkValue?: APIConsumer.PKValueType): Promise<APIConsumer.FormDefinition> {
    // This is a new value => cannot use pkValue here, use index on internalRecords
    this.ux_def.record = this.records.find((record: any) => (record[this.pkName] === pkValue));
    return this.formDefinition;
  }

  private getRecord(pk: APIConsumer.PKValueType) {
    /**
     * Get external record from its internal representation
     */
    return this.records.find((element: any) => (element[this.pkName] === pk));
  }

  private getFormUXDefinition = (pk: APIConsumer.PKValueType): APIConsumer.FormUXDefinition => ({
    primary_key_name: this.ux_def.primary_key_name,
    titles: this.ux_def.titles,
    dialog: this.ux_def.dialog,
    actions: this.ux_def.actions,
    record: this.getRecord(pk),
  });

  async dialogForm(
    pk: APIConsumer.PKValueType,
  ) {
    const result = await FormConsumerOneShotArray(
      {
        definition: this.getFormUXDefinition(pk),
        data: this.records,
        pk,
        pkName: this.pkName,
        record: this.getRecord(pk),
      },
      this.dialogHandlers,
    );

    await nextTick();
    await this.reload();

    return result;
  }

  async deleteRow(tableRow: FormPayload) {
    const element = this.records.find((record: any) => (record[this.pkName] === tableRow[this.pkName]));
    if (element) {
      this.records.splice(element.index, 1);
    }
    await this.reload();
  }
}

export default ConsumerLogicArray;
