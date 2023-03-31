import FormPayload from '../form/definitions/form-payload';
import FormLayout from '../form/definitions/layout';
import dfModal from '../modal/modal-view-api';
import OrderingDirection from '../table/definitions/column-ordering-direction';
import TableRows from '../table/definitions/rows';
import getObjectFromPath from '../util/get-object-from-path';

import BaseConsumerLogic from './base-consumer-logic';

class ConsumerLogic extends BaseConsumerLogic implements APIConsumer.MemoryLogicInterface {
  private readonly records: any;

  private internalRecords: any[];

  constructor(UXDefinition: APIConsumer.TableUXDefinition, records: any[]) {
    super();

    this.ux_def = UXDefinition;
    this.records = records;

    this.internalRecords = [];

    this.processUXDefinition(this.ux_def);
    this.reload().then(() => {}); // kind of await / not really
  }

  createRowRecords(): void {
    /**
     * Creates internal representation of records with pointers to external structure
     */
    let negativeCounter = 0;
    this.internalRecords = [...this.records].map((element: any, index: number) => ({
      ...element,
      ...{
        [this.pkName]: element[this.pkName] ?? -(++negativeCounter),
        index, // get the reference to reactive records
      },
    }));
  }

  order(): any[] {
    /**
     * Order internal records according to filters
     */
    const orderingTransformationFunction = getObjectFromPath(this.ordering.style);
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
    // TODO: do filtering
    if (filter) {
      throw new Error('Not implemented');
    }
    this.createRowRecords();
    this.order();
    this.rows = new TableRows(this, this.internalRecords);
  }

  async getFormDefinition(pkValue?: APIConsumer.PKValueType): Promise<APIConsumer.FormDefinition> {
    // This is a new value => cannot use pkValue here, use index on internalRecords
    this.ux_def.record = this.internalRecords.find((record: any) => (record[this.pkName] === pkValue));
    return this.processFormDefinition(pkValue);
  }

  private getRecord(pk: APIConsumer.PKValueType) {
    /**
     * Get external record from its internal representation
     */
    const record = this.internalRecords.find((element: any) => (element[this.pkName] === pk));
    return this.records[record.index];
  }

  async saveForm(refresh: boolean = true) {
    if (this.pkValue !== 'new' && this.pkValue) {
      // we are updating a record
      const record = this.getRecord(this.pkValue);
      for (const [key, value] of Object.entries(this.formData)) {
        record[key] = value;
      }
    } else {
      // create new record
      this.records.push({ ...this.formData });
    }
    if (refresh) {
      await this.reload();
    }
  }

  async dialogForm(pk: APIConsumer.PKValueType, formData: any = null, refresh: boolean = true) {
    const formDef = await this.getFormDefinition(pk);
    // if dialog is reopened use the old form's data
    if (formData !== null) {
      // TODO: there is currently an issue where if you get a 400 and have to fix the data, second "save" does nothing
      formDef.payload = new FormPayload(formData, this.formLayout as FormLayout);
      this.formData = formDef.payload;
    }
    const resultAction = await dfModal.fromFormDefinition(formDef);
    if (resultAction.action.name === 'submit') {
      // we want to save the record
      await this.saveForm(refresh);
    }
  }

  async deleteRow(tableRow: FormPayload) {
    const element = this.internalRecords.find((record: any) => (record[this.pkName] === tableRow[this.pkName]));
    if (element) {
      this.records.splice(element.index, 1);
    }
    await this.reload();
  }
}

export default ConsumerLogic;
