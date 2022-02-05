import apiClient from '../util/api_client';

import { TableColumns } from './table_column';
import TableRows from './table_rows';

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
    this.formFields = {};
    this.formLayout = {};
    this.actions = {};
    this.rows = [];
    this.formData = {};
  }

  async fetch(url, isTable) {
    let headers = {};
    if (isTable) headers = { 'x-viewmode': 'TABLE_ROW', 'x-pagination': 1 };
    try {
      // TODO: this does not take into account current filtering and ordering for the table
      this.loading = true;
      return (await apiClient.get(url, { headers })).data;
    } catch (err) {
      console.error('Error retrieving component def');
      throw err;
    } finally {
      this.loading = false;
    }
  }

  async getUXDefinition(isTable) {
    return this.fetch(`${this.baseURL}.componentdef`, isTable);
  }

  async getFullDefinition() {
    const UXDefinition = await this.getUXDefinition(true);
    this.titles = UXDefinition.titles;
    this.pkName = UXDefinition.primary_key_name;
    UXDefinition.columns.forEach((column) => { this.fields[column.name] = column; });
    this.tableColumns = TableColumns(UXDefinition.columns.map((col) => col.name), this.fields);
    this.rows = new TableRows(this, UXDefinition.rows);
  }

  title(which) {
    return this.titles[which];
  }
}

export default APIConsumerLogic;
