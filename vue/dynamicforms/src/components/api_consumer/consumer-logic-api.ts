import { RawAxiosRequestHeaders } from 'axios';

import { ViewSetApi } from '../api_view';
import FormPayload from '../form/definitions/form-payload';
import dfModal from '../modal/modal-view-api';
import TableRows from '../table/definitions/rows';
import apiClient from '../util/api-client';

import ConsumerLogicBase from './consumer-logic-base';
import { APIConsumer } from './namespace';

class ConsumerLogicApi extends ConsumerLogicBase implements APIConsumer.ConsumerLogicAPIInterface {
  private readonly baseURL: string;

  private readonly trailingSlash: boolean;

  private readonly api: ViewSetApi<any>;

  constructor(baseURL: string, trailingSlash: boolean = true) {
    super();
    /**
     * baseURL points to the API entry point, basically the GET / LIST endpoint. We will be composing all the other
     * endpoints from this one
     */
    this.baseURL = baseURL.replace(/\/$/, ''); // remove trailing slash if it was there
    this.api = new ViewSetApi<any>(baseURL, trailingSlash);
    this.trailingSlash = trailingSlash;
  }

  async fetch() {
    try {
      // TODO: this does not take into account current filtering and ordering for the table
      this.loading = true;
      const orderingParams = {} as any;
      const orderingValue = this.tableColumns[0].ordering.calculateOrderingValue();
      if (orderingValue.length) {
        orderingParams[this.ordering.parameter] = `${orderingValue}`;
      }
      return (await this.api.list({ params: { ...orderingParams, ...this.filterData } }));
    } catch (err) {
      console.error('Error retrieving component def');
      throw err;
    } finally {
      this.loading = false;
    }
  }

  async fetchNewRows(url: string) {
    const headers: RawAxiosRequestHeaders = { 'x-viewmode': 'TABLE_ROW', 'x-pagination': 1 };
    try {
      this.loading = true;
      const orderingParams = {} as any;
      const orderingValue = this.tableColumns[0].ordering.calculateOrderingValue();
      if (orderingValue.length) {
        orderingParams[this.ordering.parameter] = `${orderingValue}`;
      }
      return (await apiClient.get(url, {
        headers,
        params: { ...orderingParams, ...this.filterData },
        showProgress: false,
      })).data;
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

  async reload() {
    this.rows = new TableRows(
      this,
      await this.fetch(),
    );
  }

  async getRecord(pkValue: string) {
    if (pkValue || pkValue !== 'new') {
      return this.api.retrieve(pkValue);
    }
    return this.api.list();
  }

  async getUXDefinition(pkValue?: APIConsumer.PKValueType): Promise<APIConsumer.TableUXDefinition> {
    return this.api.componentDefinition(pkValue);
  }

  async getFullDefinition() {
    const UXDefinition = await this.getUXDefinition(null);
    this.processUXDefinition(UXDefinition);
  }

  async getFormDefinition(pkValue?: APIConsumer.PKValueType): Promise<APIConsumer.FormDefinition> {
    if (this.formLayout == null) {
      this.ux_def = await this.getUXDefinition(pkValue);
      this.pkName = this.ux_def.primary_key_name;
      this.titles = this.ux_def.titles;
      // TODO: actions = UXDefinition.dialog.actions (merge with fulldefinition.actions)
    } else {
      // reread the current record
      this.ux_def.record = await this.getRecord(pkValue);
    }
    return this.formDefinition;
  }

  async delete() {
    if (this.pkValue && this.pkValue !== 'new') {
      await this.api.delete(this.pkValue);
    }
  }

  async deleteRow(tableRow: FormPayload) {
    const pkValue = tableRow[this.pkName];
    await this.api.delete(pkValue);
    this.rows.deleteRow(pkValue);
  }

  async saveForm(refresh: boolean = true) {
    let res;

    if (this.pkValue !== 'new' && this.pkValue) {
      res = await this.api.update(this.pkValue, this.formData);
    } else {
      // this.pkValue might be new or null for SingleRecordViewSets
      res = await this.api.create(this.formData);
    }

    if (refresh) {
      // reload the whole table
      await this.reload();
    }

    return res;
  }

  async dialogForm(
    pk: APIConsumer.PKValueType,
    formData: any = null,
    refresh: boolean = true,
    return_raw_data: boolean = false,
  ) {
    const formDef = await this.getFormDefinition(pk);
    // if dialog is reopened use the old form's data
    if (formData !== null) {
      // TODO: there is currently an issue where if you get a 400 and have to fix the data, second "save" does nothing
      // eslint-disable-next-line array-callback-return
      Object.entries(formData).map(([key, value]) => { formDef.payload[key] = value; });
      this.formData = formDef.payload;
    }
    const resultAction = await dfModal.fromFormDefinition(formDef);
    if (return_raw_data) {
      // we don't want to process the data, so we just return it as it came in. useful for file downloads and such
      return { action: resultAction.action, data: this.formData };
    }
    let error = {};
    let result: any;
    if (resultAction.action.name === 'submit') {
      try {
        result = await this.saveForm(refresh);
      } catch (err: any) {
        // Include form error and field errors
        error = { ...err?.response?.data };
      }
    } else if (resultAction.action.name === 'delete_dlg') {
      try {
        result = await this.delete();
      } catch (err: any) {
        // Include form error and field errors
        error = { ...err.response.data };
      }
    }
    // propagate error to the next dialog
    this.errors = error;
    // open new dialog if needed
    if (error && Object.keys(error).length) result = await this.dialogForm(pk, this.formData, refresh);
    return result;
  }
}

export default ConsumerLogicApi;
