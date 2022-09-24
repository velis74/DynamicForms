import _ from 'lodash';

import FilteredActions from '../actions/filtered-actions';
import FormPayload from '../form/definitions/form-payload';
import FormLayout from '../form/definitions/layout';
import TableColumns from '../table/definitions/columns';
import TableFilterRow from '../table/definitions/filterrow';
import TableRows from '../table/definitions/rows';
import apiClient from '../util/api-client';
import getObjectFromPath from '../util/get-object-from-path';

class APIConsumerLogic {
  constructor(baseURL) {
    /**
     * baseURL points to the API entry point, basically the GET / LIST endpoint. We will be composing all the other
     * endpoints from this one
     */
    this.baseURL = baseURL.replace(/\/$/, ''); // remove trailing slash if it was there

    /**
     * pkName specifies the primary key for the table. This field is expected to be unique and will be used to uniquely
     * identify rows as they are returned from the API. Based on this uniqueness, we can find and refresh existing rows.
     */
    this.pkName = 'id';

    /**
     * loading = true when loading new data. Use this in component to indicate / display a loader
     */
    this.loading = false;

    this.fields = {};
    this.tableColumns = [];
    this.responsiveTableLayouts = null;
    this.formFields = {};
    this.formLayout = null;
    this.formComponent = 'FormLayout'; // component responsible for rendering the form layout
    this.actions = {};
    this.rows = [];
    this.formData = {};
    this.requestedPKValue = null;
    this.ordering = {
      parameter: 'ordering',
      style: null,
      counter: 0,
    };
    this.filterDefinition = null;
    this.filterData = {};
  }

  async fetch(url, isTable, filter = false) {
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

  formatUrlWithOrderParam(url) {
    let requestUrl = url;
    const orderingTransformationFunction = getObjectFromPath(this.ordering_style);
    const orderingValue = this.tableColumns[0].ordering.calculateOrderingValue(orderingTransformationFunction);
    const order = orderingValue.length ? `${this.ordering.parameter}=${orderingValue}` : '';
    if (order.length) requestUrl = `${url}?${order}`;
    return requestUrl;
  }

  async reload(filter = false) {
    this.rows = new TableRows(this,
      await this.fetch(this.formatUrlWithOrderParam(`${this.baseURL}.json`), true, filter));
  }

  async getUXDefinition(pkValue, isTable) {
    let url = this.baseURL;
    if (!isTable) url += `/${pkValue}`;
    return this.fetch(`${url}.componentdef`, isTable);
  }

  async getRecord(pkValue) {
    const url = `${this.baseURL}/${pkValue}.json`;
    return (await apiClient.get(url)).data;
  }

  async getFullDefinition() {
    const UXDefinition = await this.getUXDefinition(null, true);
    this.pkName = UXDefinition.primary_key_name;
    this.titles = UXDefinition.titles;
    UXDefinition.columns.forEach((column) => {
      this.fields[column.name] = column;
    });
    this.tableColumns = TableColumns(UXDefinition.columns.map((col) => col.name), this.fields);
    this.rows = new TableRows(this, UXDefinition.rows);
    this.setOrdering(
      UXDefinition.ordering_parameter,
      UXDefinition.ordering_style,
      this.tableColumns[0].ordering.changeCounter,
    );
    this.responsiveTableLayouts = UXDefinition.responsive_table_layouts;
    this.actions = new FilteredActions(UXDefinition.actions);
    // TODO: actions = UXDefinition.actions (merge with formdefinition.actions)
    this.filterDefinition = new TableFilterRow(UXDefinition.filter);
  }

  async getFormDefinition(pkValue) {
    if (this.formLayout == null) {
      const UXDefinition = await this.getUXDefinition(pkValue, false);
      this.requestedPKValue = pkValue;
      this.pkName = UXDefinition.primary_key_name;
      this.titles = UXDefinition.titles;
      this.formLayout = new FormLayout(UXDefinition.dialog);
      this.formData = new FormPayload(UXDefinition.record, this.formLayout);
      this.actions = new FilteredActions(UXDefinition.actions);
      // TODO: actions = UXDefinition.dialog.actions (merge with fulldefinition.actions)
    } else {
      // reread the current record
      const record = await this.getRecord(this.pkValue);
      this.formData = new FormPayload(record, this.formLayout);
    }
  }

  setOrdering(parameter, style, counter) {
    this.ordering = { parameter: parameter || 'ordering', style, counter };
  }

  title(which) {
    return this.titles[which];
  }

  get tableDefinition() {
    return {
      title: this.title('table'),
      pkName: this.pkName,
      columns: this.tableColumns,
      responsiveTableLayouts: this.responsiveTableLayouts,
      columnDefs: this.fields,
      rows: this.rows,
      loading: this.loading,
      actions: this.actions,
      filterDefinition: this.filterDefinition,
    };
  }

  get pkValue() {
    return this.requestedPKValue === 'new' ? 'new' : (this.formData || {})[this.pkName];
  }

  get formDefinition() {
    return {
      title: this.title(this.pkValue === 'new' ? 'new' : 'edit'),
      pkName: this.pkName,
      pkValue: this.pkValue,
      layout: this.formLayout,
      payload: this.formData,
      loading: this.loading,
      actions: this.actions,
    };
  }

  async deleteRow(tableRow) {
    await apiClient.delete(`${this.baseURL}/${tableRow[this.pkName]}/`);
    this.rows.deleteRow(tableRow[this.pkName]);
  }

  async saveForm() {
    let url = `${this.baseURL}/`;
    let res;

    if (this.pkValue !== 'new') {
      url += `${this.pkValue}/`;
      res = await apiClient.put(url, this.formData);
    } else {
      res = await apiClient.post(url, this.formData);
    }
    // TODO: update any table here too, either add the new record or modify the existing one
    console.warn('table processing not done yet: here we should append / update the table row', res);
  }

  async dialogForm(pk, dfModal) {
    await this.getFormDefinition(pk);
    const resultAction = await dfModal.fromFormDefinition(this.formDefinition);
    if (resultAction.action.name === 'submit') {
      await this.saveForm();
      // TODO: catch 400 here and show the dialog again
    }
  }

  async filter(filterData) {
    // eslint-disable-next-line max-len,no-unused-expressions
    !_.includes(['', undefined, null], filterData.newValue) ? this.filterData[filterData.field] = filterData.newValue : delete this.filterData[filterData.field];
    await this.reload(true);
  }
}

export default APIConsumerLogic;
