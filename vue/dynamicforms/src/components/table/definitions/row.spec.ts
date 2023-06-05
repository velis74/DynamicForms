import { DfTable } from '../namespace';

import TableRow from './row';

describe('TableRow', () => {
  let rowData: DfTable.RowDataInterface;

  beforeEach(() => {
    rowData = {
      id: 1,
      name: 'test',
      df_control_data: {
        row_css_class: 'even',
        row_css_style: 'background-color: lightblue',
        // actions?: any[];
      },
    };
  });

  it('should create a TableRow object correctly', () => {
    const tableRow = new TableRow(rowData);

    // assert that tableRow properties match expected values
    expect(tableRow.id).toBe(1);
    expect(tableRow.name).toBe('test');

    expect(tableRow.dfControlStructure.isShowing).toBe(true);
    expect(tableRow.dfControlStructure.measuredHeight).toBeNull();
    expect(tableRow.dfControlStructure.componentName).toBe('GenericTRow');
    expect(tableRow.dfControlStructure.CSSClass).toBe('even');
    expect(tableRow.dfControlStructure.CSSStyle).toBe('background-color: lightblue');
  });

  it('should create a TableRow object correctly when df_control_data is not provided', () => {
    const tableRow = new TableRow({ id: 1, name: 'test' });

    // assert that tableRow properties match expected values
    expect(tableRow.id).toBe(1);
    expect(tableRow.name).toBe('test');

    expect(tableRow.dfControlStructure.isShowing).toBe(true);
    expect(tableRow.dfControlStructure.measuredHeight).toBeNull();
    expect(tableRow.dfControlStructure.componentName).toBe('GenericTRow');
    expect(tableRow.dfControlStructure.CSSClass).toBe('');
    expect(tableRow.dfControlStructure.CSSStyle).toBe('');
  });

  it('should set measuredHeight correctly', () => {
    const tableRow = new TableRow(rowData);
    const newValue = 100;
    tableRow.setMeasuredHeight(newValue);

    expect(tableRow.dfControlStructure.measuredHeight).toBe(newValue);
  });

  it('should set isShowing correctly', () => {
    const tableRow = new TableRow(rowData);
    const newValue = false;
    tableRow.setIsShowing(newValue);

    expect(tableRow.dfControlStructure.isShowing).toBe(newValue);
  });
});
