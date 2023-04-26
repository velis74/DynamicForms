import FormPayload from '../form/definitions/form-payload';
import FormLayout from '../form/definitions/layout';
import dfModal from '../modal/modal-view-api';
import TableRows from '../table/definitions/rows';
import apiClient from '../util/api-client';

import ConsumerLogicBase from './consumer-logic-base';
import { APIConsumer } from './namespace';

class ConsumerLogicApi extends ConsumerLogicBase implements APIConsumer.ConsumerLogicAPIInterface {
  private readonly baseURL: string;

  constructor(baseURL: string) {
    super();
    /**
     * baseURL points to the API entry point, basically the GET / LIST endpoint. We will be composing all the other
     * endpoints from this one
     */
    this.baseURL = baseURL.replace(/\/$/, ''); // remove trailing slash if it was there
  }

  async fetch(url: string, isTable: boolean, filter: boolean = false) {
    let headers = {};
    if (isTable) headers = { 'x-viewmode': 'TABLE_ROW', 'x-pagination': 1 };
    try {
      // TODO: this does not take into account current filtering and ordering for the table
      this.loading = true;
      let requestUrl = url;
      if (filter) {
        requestUrl = this.formatUrlWithOrderParam(`${this.baseURL}.json`);
      }
      return (await apiClient.get(requestUrl, { headers, params: this.filterData })).data;
    } catch (err) {
      console.error('Error retrieving component def');
      throw err;
    } finally {
      this.loading = false;
    }
  }

  formatUrlWithOrderParam(url: string) {
    let requestUrl = url;
    const orderingValue = this.tableColumns[0].ordering.calculateOrderingValue();
    const order = orderingValue?.length ? `${this.ordering.parameter}=${orderingValue}` : '';
    if (order.length) requestUrl = `${url}?${order}`;
    return requestUrl;
  }

  async reload(filter: boolean = false) {
    this.rows = new TableRows(
      this,
      await this.fetch(this.formatUrlWithOrderParam(`${this.baseURL}.json`), true, filter),
    );
  }

  async getRecord(pkValue: string) {
    const url = `${this.baseURL}/${pkValue}.json`;
    return (await apiClient.get(url)).data;
  }

  async getUXDefinition(pkValue: APIConsumer.PKValueType, isTable: boolean): Promise<APIConsumer.TableUXDefinition> {
    let url = this.baseURL;
    if (!isTable && pkValue) url += `/${pkValue}`;
    return this.fetch(`${url}.componentdef`, isTable);
  }

  async getFullDefinition() {
    const UXDefinition = await this.getUXDefinition(null, true);
    this.processUXDefinition(UXDefinition);
  }

  async getFormDefinition(pkValue?: APIConsumer.PKValueType): Promise<APIConsumer.FormDefinition> {
    if (this.formLayout == null) {
      this.ux_def = await this.getUXDefinition(pkValue, false);
      this.pkName = this.ux_def.primary_key_name;
      this.titles = this.ux_def.titles;
      // TODO: actions = UXDefinition.dialog.actions (merge with fulldefinition.actions)
    } else {
      // reread the current record
      this.ux_def.record = await this.getRecord(pkValue);
    }
    return this.processFormDefinition(pkValue);
  }

  async delete() {
    if (this.pkValue !== 'new') {
      await apiClient.delete(`${this.baseURL}/${this.pkValue}`);
    }
  }

  async deleteRow(tableRow: FormPayload) {
    await apiClient.delete(`${this.baseURL}/${tableRow[this.pkName]}/`);
    this.rows.deleteRow(tableRow[this.pkName]);
  }

  async saveForm(refresh: boolean = true) {
    let res;

    if (this.pkValue !== 'new' && this.pkValue) {
      res = await apiClient.put(`${this.baseURL}/${this.pkValue}/`, this.formData);
    } else {
      // this.pkValue might be new or null for SingleRecordViewSets
      res = await apiClient.post(`${this.baseURL}${this.pkValue ? '/' : ''}`, this.formData);
    }

    if (refresh) {
      // reload the whole table
      await this.reload(true);
    }

    return res;
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
    let error = {};
    if (resultAction.action.name === 'submit') {
      try {
        await this.saveForm(refresh);
      } catch (err: any) {
        // Include form error and field errors
        error = { ...err?.response?.data };
      }
    } else if (resultAction.action.name === 'delete_dlg') {
      await this.delete().catch((data) => {
        // Include form error and field errors
        error = { ...data.response.data };
      });
    }
    // propagate error to the next dialog
    this.errors = error;
    // open new dialog if needed
    if (error && Object.keys(error).length) await this.dialogForm(pk, this.formData);
  }
}

export default ConsumerLogicApi;
