import { DfTable } from '../namespace';

import TableColumn from './column';
import ColumnOrdering from './column-ordering';
import OrderingDirection from './column-ordering-direction';

type ColumnJSON = DfTable.ColumnJSON;

describe('ColumnOrdering', () => {
  let orderingArray: ColumnOrdering[];

  beforeEach(() => {
    orderingArray = [];
  });

  test('returns the correct ordering array for the given one column', () => {
    const columnsData: ColumnJSON[] = [
      // Define your columns here
      // Example column:
      {
        name: 'id',
        label: 'ID',
        table_classes: '',
        ordering: 'ordering asc seg-1',
        alignment: 'right',
        visibility: {
          table: 10,
          form: 5,
        },
        render_params: {
          form_component_name: 'DInput',
          input_type: 'number',
          table: 'df-tablecell-plaintext',
          field_class: 'form-control',
        },
      },
    ];

    columnsData.map((columnData) => new TableColumn(columnData, orderingArray));

    // Assert the ordering array is correct based on your columns
    expect(orderingArray.length).toEqual(1);
    // Assert individual members of orderingArray
    expect(orderingArray[0].changeCounter).toBe(0);
    expect(orderingArray[0].direction).toBe(1);
    expect(orderingArray[0].isOrderable).toBe(true);
    expect(orderingArray[0].isOrdered).toBe(true);
    expect(orderingArray[0].segment).toBe(1);
  });
  test('returns the correct ordering array for the given columns', () => {
    const columnsData: ColumnJSON[] = [
      // Define your columns here
      // Example column:
      {
        name: 'id',
        label: 'ID',
        table_classes: '',
        ordering: 'ordering asc seg-1',
        alignment: 'right',
        visibility: {
          table: 10,
          form: 5,
        },
        render_params: {
          form_component_name: 'DInput',
          input_type: 'number',
          table: 'df-tablecell-plaintext',
          field_class: 'form-control',
        },
      },
      {
        name: 'enabled',
        label: 'Enabled',
        alignment: 'left',
        visibility: {
          table: 10,
          form: 10,
        },
        render_params: {
          form_component_name: 'DCheckbox',
          input_type: 'checkbox',
          table: 'df-tablecell-bool',
          field_class: 'form-check-input position-checkbox-static',
        },
        ordering: 'ordering desc seg-3',
      },
      {
        name: 'email_field',
        label: 'Email field',
        table_classes: '',
        ordering: 'ordering asc seg-2',
        alignment: 'left',
        visibility: {
          table: 10,
          form: 10,
        },
        render_params: {
          form_component_name: 'DInput',
          input_type: 'email',
          table: 'df-tablecell-email',
          field_class: 'form-control',
        },
      },
      {
        name: 'url_field',
        label: 'Url field',
        table_classes: '',
        ordering: 'ordering unsorted',
        alignment: 'left',
        visibility: {
          table: 10,
          form: 10,
        },
        render_params: {
          form_component_name: 'DInput',
          input_type: 'url',
          table: 'df-tablecell-link',
          pattern: 'https?://.*',
          field_class: 'form-control',
        },
      },
      {
        name: 'ipaddress_field',
        label: 'Ipaddress field',
        table_classes: '',
        ordering: '',
        alignment: 'left',
        visibility: {
          table: 10,
          form: 10,
        },
        render_params: {
          form_component_name: 'DInput',
          input_type: 'text',
          table: 'df-tablecell-ipaddr',
        },
      },
    ];

    columnsData.map((columnData) => new TableColumn(columnData, orderingArray));

    // Assert the ordering array is correct based on your columns
    expect(orderingArray.length).toEqual(3);
    // Assert individual members of orderingArray
    expect(orderingArray[0].changeCounter).toBe(0);
    expect(orderingArray[0].direction).toBe(1);
    expect(orderingArray[0].isOrderable).toBe(true);
    expect(orderingArray[0].isOrdered).toBe(true);
    expect(orderingArray[0].segment).toBe(1);

    expect(orderingArray[1].changeCounter).toBe(0);
    expect(orderingArray[1].direction).toBe(1);
    expect(orderingArray[1].isOrderable).toBe(true);
    expect(orderingArray[1].isOrdered).toBe(true);
    expect(orderingArray[1].segment).toBe(2);

    expect(orderingArray[2].changeCounter).toBe(0);
    expect(orderingArray[2].direction).toBe(2);
    expect(orderingArray[2].isOrderable).toBe(true);
    expect(orderingArray[2].isOrdered).toBe(true);
    expect(orderingArray[2].segment).toBe(3);
  });

  test('cycle ordering', () => {
    const columnsData: ColumnJSON[] = [
      // Define your columns here
      // Example column:
      {
        name: 'id',
        label: 'ID',
        table_classes: '',
        ordering: 'ordering asc seg-1',
        alignment: 'right',
        visibility: {
          table: 10,
          form: 5,
        },
        render_params: {
          form_component_name: 'DInput',
          input_type: 'number',
          table: 'df-tablecell-plaintext',
          field_class: 'form-control',
        },
      },
    ];

    columnsData.map((columnData) => new TableColumn(columnData, orderingArray));

    // Assert the ordering array is correct based on your columns
    expect(orderingArray.length).toEqual(1);

    // Assert individual members of orderingArray
    expect(orderingArray[0].changeCounter).toBe(0);
    expect(orderingArray[0].direction).toBe(OrderingDirection.ASC);
    expect(orderingArray[0].isOrderable).toBe(true);
    expect(orderingArray[0].isOrdered).toBe(true);
    expect(orderingArray[0].segment).toBe(1);

    [[OrderingDirection.DESC, true], [OrderingDirection.UNORDERED, false], [OrderingDirection.ASC, true]]
      .forEach(([direction, isOrdered]) => {
        orderingArray[0].cycleOrdering();
        expect(orderingArray[0].direction).toBe(direction);
        expect(orderingArray[0].isOrdered).toBe(isOrdered);
      });
  });
});
