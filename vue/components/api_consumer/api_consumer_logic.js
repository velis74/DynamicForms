import apiClient from '../util/api_client';

import { TableColumns } from './table_column';

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
    this.fields = {};
    this.tableColumns = [];
    this.formFields = {};
    this.formLayout = {};
    this.actions = {};
    this.rows = [];
    this.formData = {};
  }

  async getUXDefinition(isTable) {
    let headers = {};
    if (isTable) headers = { 'x-viewmode': 'TABLE_ROW', 'x-pagination': 1 };
    try {
      // TODO: this does not take into account current filtering and ordering for the table
      return (await apiClient.get(`${this.baseURL}.componentdef`, { headers })).data;
    } catch (err) {
      console.error('Error retrieving component def');
      throw err;
    }
  }

  async getFullDefinition() {
    const UXDefinition = await this.getUXDefinition(true);
    this.titles = UXDefinition.titles;
    this.pkName = UXDefinition.primary_key_name;
    UXDefinition.columns.forEach((column) => { this.fields[column.name] = column; });
    this.tableColumns = TableColumns(UXDefinition.columns.map((col) => col.name), this.fields);
    this.rows = UXDefinition.rows.results;
  }

  title(which) {
    return this.titles[which];
  }
}

export default APIConsumerLogic;
