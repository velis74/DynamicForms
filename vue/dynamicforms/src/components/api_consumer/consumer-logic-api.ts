import { RawAxiosRequestHeaders } from 'axios';
import { Ref } from 'vue';

import { ViewSetApi } from '../api_view';
import FormPayload from '../form/definitions/form-payload';
import TableRows from '../table/definitions/rows';
import apiClient from '../util/api-client';

import ConsumerLogicBase from './consumer-logic-base';
import FormConsumerApiOneShot from './form-consumer/api-one-shot';
import type { APIConsumer } from './namespace';

class ConsumerLogicApi extends ConsumerLogicBase implements APIConsumer.ConsumerLogicAPIInterface {
  private readonly trailingSlash: boolean;

  private readonly baseUrl: string | Ref<string>;

  private readonly api: ViewSetApi<any>;

  private requestId: number = 0;

  constructor(baseURL: string | Ref<string>, trailingSlash: boolean = true) {
    super();
    /**
     * baseURL points to the API entry point, basically the GET / LIST endpoint. We will be composing all the other
     * endpoints from this one
     */
    this.api = new ViewSetApi<any>(baseURL, trailingSlash);

    /** Utilities for form consumer  */
    this.baseUrl = baseURL;
    this.trailingSlash = trailingSlash;
  }

  async fetch(url?: string) {
    const reqId = ++this.requestId;
    let result;
    if (url !== undefined) {
      result = await this.fetchNewRows(url);
    } else {
      result = await this.fetchRecords();
    }
    if (this.requestId === reqId) {
      // we are the latest request to the backend
      return result;
    }
    return undefined;
  }

  async fetchRecords() {
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
    const result = await this.fetch();
    if (result) {
      this.rows = new TableRows(
        this,
        result,
      );
    }
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
    this.requestedPKValue = pkValue;
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

  async deleteRow(tableRow: FormPayload) {
    const pkValue = tableRow[this.pkName];
    await this.api.delete(pkValue);
    this.rows.deleteRow(pkValue);
  }

  async dialogForm(
    pk: APIConsumer.PKValueType,
    formData: any = null,
  ) {
    Object.assign(this.formData, formData);

    const result = await FormConsumerApiOneShot(
      this.baseUrl,
      this.trailingSlash,
      pk,
      this.formData,
    );

    await this.reload();

    return result;
  }
}

export default ConsumerLogicApi;
