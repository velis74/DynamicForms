import { AxiosError, RawAxiosRequestHeaders } from 'axios';
import { Ref } from 'vue';

import { ViewSetApi } from '../adapters/api';
import FormPayload from '../form/definitions/form-payload';
import { showNotificationFromAxiosException } from '../notifications';

import ConsumerLogicBase from './consumer-logic-base';
import FormConsumerOneShotApi from './form-consumer/one-shot/api';
import type { APIConsumer } from './namespace';

import { apiClient } from '@/util';

class ConsumerLogicApi extends ConsumerLogicBase implements APIConsumer.ConsumerLogicAPIInterface {
  protected readonly trailingSlash: boolean;

  protected readonly baseUrl: string | Ref<string>;

  protected readonly api: ViewSetApi<any>;

  protected requestId: number = 0;

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
    if (result) this.rows.replaceRows(result);
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
    try {
      await this.api.delete(pkValue);
      this.rows.deleteRow(pkValue);
    } catch (e) {
      if (e instanceof AxiosError) {
        showNotificationFromAxiosException(e);
      } else {
        console.error('Unexpected error', e);
      }
    }
  }

  async dialogForm(
    pk: APIConsumer.PKValueType,
  ) {
    const result = await FormConsumerOneShotApi(
      {
        url: this.baseUrl,
        trailingSlash: this.trailingSlash,
        pk,
      },
      this.dialogHandlers,
    );
    if (result) this.rows.updateRows([result]);

    return result;
  }
}

export default ConsumerLogicApi;
