import FilteredActions from '../actions/filtered-actions';
import { ActionsNS } from '../actions/namespace';
import FormPayload from '../form/definitions/form-payload';
import FormLayout from '../form/definitions/layout';
import TableColumns from '../table/definitions/columns';
import TableFilterRow from '../table/definitions/filterrow';
import TableRows from '../table/definitions/rows';
import { DfTable } from '../table/namespace';

import { APIConsumer } from './namespace';

abstract class ConsumerLogicBase implements APIConsumer.ConsumerLogicBaseInterface {
  pkName: string;

  protected fields: { [key: string]: DfTable.ColumnJSON };

  protected tableColumns: TableColumns;

  protected loading: boolean;

  protected responsiveTableLayouts?: DfTable.ResponsiveTableLayoutsDefinition;

  protected formFields: { [key: string]: unknown };

  protected formLayout: FormLayout | null;

  protected formComponent: string; // component responsible for rendering the form layout

  protected errors: { [key: string]: unknown };

  protected actions: FilteredActions;

  protected ux_def: APIConsumer.TableUXDefinition;

  protected rows: TableRows;

  protected formData: FormPayload;

  protected requestedPKValue: null;

  protected ordering: { parameter: string, style: string | undefined, counter: number };

  protected filterDefinition: TableFilterRow | null;

  public filterData: Object;

  protected titles: APIConsumer.Titles;

  protected constructor() {
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
    this.tableColumns = new TableColumns([], {});
    this.responsiveTableLayouts = undefined;
    this.formFields = {};
    this.formLayout = null;
    this.formComponent = 'df-form-layout';
    this.errors = {};
    this.actions = new FilteredActions({});
    this.ux_def = {} as APIConsumer.TableUXDefinition;
    this.rows = new TableRows(this, []);
    this.formData = {} as any;
    this.requestedPKValue = null;
    this.ordering = {
      parameter: 'ordering',
      style: undefined,
      counter: 0,
    };
    this.filterDefinition = null;
    this.filterData = {};
    this.titles = { new: '', edit: '', table: '' };
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
    return this.requestedPKValue === 'new' || this.requestedPKValue == null ?
      this.requestedPKValue : this.formData?.[this.pkName];
  }

  /** @virtual */
  processUXDefinition(UXDefinition: APIConsumer.TableUXDefinition): void {
    /**
     * Takes UXDefinition and saves certain fields into internal values
     */
    this.pkName = UXDefinition.primary_key_name;
    this.titles = UXDefinition.titles;
    UXDefinition.columns.forEach((column) => {
      this.fields[column.name] = column;
    });
    this.tableColumns = new TableColumns(UXDefinition.columns.map((col: any) => col.name), this.fields);
    this.rows = new TableRows(this, UXDefinition.rows);
    this.setOrdering(
      UXDefinition.ordering_parameter,
      UXDefinition.ordering_style,
      this.tableColumns[0].ordering.changeCounter,
    );
    this.responsiveTableLayouts = UXDefinition.responsive_table_layouts;
    this.actions = new FilteredActions(<ActionsNS.ActionsJSON> UXDefinition.actions);
    // TODO: actions = UXDefinition.actions (merge with formdefinition.actions)
    this.filterDefinition = new TableFilterRow(UXDefinition.filter);
  }

  abstract getFormDefinition(pkValue?: APIConsumer.PKValueType): Promise<APIConsumer.FormDefinition>;

  get formDefinition(): APIConsumer.FormDefinition {
    // this.requestedPKValue = this.pkValue;
    this.formLayout = new FormLayout(this.ux_def.dialog);
    this.formData = new FormPayload(this.ux_def.record, this.formLayout);
    this.actions = new FilteredActions(this.ux_def.actions);
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

  title(which: 'table' | 'new' | 'edit'): string {
    /**
     * @return Name of the form for the action we call.
     */
    return this.titles[which];
  }

  setOrdering(parameter: string, style: any | null, counter: number) {
    this.ordering = { parameter: parameter || 'ordering', style, counter };
  }

  async filter(filterData: Object | null = null) {
    if (filterData) {
      const columns = this.filterDefinition?.columns;
      this.filterData = Object.fromEntries(Object.entries(filterData).map(([key, value]) => {
        if (columns?.[key]?.renderParams.form_component_name === 'DSelect') {
          return [key, value?.[0]];
        }
        return [key, value];
      }));
    }
    await this.reload(true);
  }

  abstract reload(filter?: boolean): Promise<void>;
  abstract dialogForm(
    pk: APIConsumer.PKValueType,
    formData?: any,
    refresh?: boolean,
    return_raw_data?: boolean,
  ): Promise<any>;
  abstract deleteRow(tableRow: FormPayload): Promise<void>;
}

export default ConsumerLogicBase;
