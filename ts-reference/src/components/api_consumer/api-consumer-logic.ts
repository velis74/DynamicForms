import FilteredActions from '../actions/filtered-actions';
import FormPayload from '../form/definitions/form-payload';
import FormLayout from '../form/definitions/layout';
import TableColumns from '../table/definitions/columns';
import TableFilterRow from '../table/definitions/filter-row';
import TableRows from '../table/definitions/rows';
import apiClient from '../util/api-client';
import getObjectFromPath from '../util/get-object-from-path';

class APIConsumerLogic {
  baseURL: string;
  private pkName: string;
  private loading: boolean;
  fields: any;
  private tableColumns: Array<any>;
  private responsiveTableLayouts: null;
  private formFields: any;
  private formLayout: FormLayout | any;
  private formComponent: string;
  private errors: any;
  private actions: any;
  private ux_def: any;
  private rows: any | TableRows;
  private formData: any;
  private requestedPKValue: any;
  ordering: { parameter: string; style: null; counter: number };
  private filterDefinition: any;
  private filterData: any;
  private ordering_style: string = '';
  private titles: any;

  constructor(baseURL: string) {
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
    this.errors = {};
    this.actions = {};
    this.ux_def = {};
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

  async fetch(url: string, isTable: boolean, filter = false) {
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

  async getUXDefinition(pkValue: any, isTable: boolean) {
    let url = this.baseURL;
    if (!isTable) url += `/${pkValue}`;
    return this.fetch(`${url}.componentdef`, isTable);
  }

  async getRecord(pkValue: any) {
    const url = `${this.baseURL}/${pkValue}.json`;
    return (await apiClient.get(url)).data;
  }

  async getFullDefinition() {
    const UXDefinition = await this.getUXDefinition(null, true);
    this.pkName = UXDefinition.primary_key_name;
    this.titles = UXDefinition.titles;
    UXDefinition.columns.forEach((column: any) => {
      this.fields[column.name] = column;
    });
    this.tableColumns = TableColumns(UXDefinition.columns.map((col: any) => col.name), this.fields);
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

  async getFormDefinition(pkValue: any) {
    if (this.formLayout == null) {
      this.ux_def = await this.getUXDefinition(pkValue, false);
      this.pkName = this.ux_def.primary_key_name;
      this.titles = this.ux_def.titles;
      // TODO: actions = UXDefinition.dialog.actions (merge with fulldefinition.actions)
    } else {
      // reread the current record
      this.ux_def.record = await this.getRecord(pkValue);
    }
    this.requestedPKValue = pkValue;
    this.formLayout = new FormLayout(this.ux_def.dialog);
    this.formData = new FormPayload(this.ux_def.record, this.formLayout);
    this.actions = new FilteredActions(this.ux_def.actions);
  }

  setOrdering(parameter: any, style: any, counter: number) {
    this.ordering = { parameter: parameter || 'ordering', style, counter };
  }

  title(which: any) {
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
      errors: this.errors,
    };
  }

  async deleteRow(tableRow: any) {
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

    // reload the whole table
    await this.reload(true);

    return res;
  }

  async dialogForm(pk: any, dfModal: any, formData = null) {
    await this.getFormDefinition(pk);
    // if dialog is reopened use the old form's data
    if (formData !== null) {
      this.formData = formData;
    }
    const resultAction = await dfModal.fromFormDefinition(this.formDefinition);
    let error = {};
    if (resultAction.action.name === 'submit') {
      await this.saveForm().catch((data) => {
        // Include form error and field errors
        error = { ...data.response.data };
      });
    }
    // propagate error to the next dialog
    this.errors = error;
    // open new dialog if needed
    if (error && Object.keys(error).length) await this.dialogForm(pk, dfModal, this.formData);
  }

  async filter(filterData = null) {
    if (filterData) this.filterData = filterData;
    await this.reload(true);
  }
}

export default APIConsumerLogic;
