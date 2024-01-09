import DisplayMode from '../../classes/display-mode';
import { DfTable } from '../namespace';

import TableColumn from './column';
import ColumnOrdering from './column-ordering';

type ColumnJSON = DfTable.ColumnJSON;

declare global {
  interface Window {
    my_lib: {
      decorator?: (rec: Record<string, any>, h: boolean) => any;
    };
  }
}

describe('TableColumn', () => {
  let orderingArray: ColumnOrdering[];
  const thead = false;
  const rowData = {
    id: 12,
    enabled: false,
    email_field: 'test@example.com',
    url_field: 'https://www.example.com',
    ipaddress_field: '192.168.0.1',
    file_field: 'example.txt',
    custom_field: 28,
  };

  beforeEach(() => {
    orderingArray = [];
  });

  test('constructor should assign properties correctly', () => {
    const initialData: ColumnJSON = {
      name: 'id',
      label: 'ID',
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
      ordering: 'ordering asc seg-1',
    };

    const column = new TableColumn(initialData, orderingArray);

    expect(column.name).toBe('id');
    expect(column.label).toBe('ID');
    expect(column.align).toBe('right');
    expect(column.visibility).toEqual(DisplayMode.FULL);
    expect(column.CSSClass).toBe('');
    expect(column.CSSClassHead).toBe('ordering');
    expect(column.renderParams).toEqual({
      form_component_name: 'DInput',
      input_type: 'number',
      table: 'df-tablecell-plaintext',
      field_class: 'form-control',
    });
    expect(column.renderComponentName).toBe('');
    expect(column.maxWidth).toBe(0);
    expect(column.CSSClassHead).toBe('ordering');

    const result = column.renderDecoratorFunction(rowData, thead);
    expect(result).toBe(12);
  });
  test('setLayout and setMaxWidth should accept their new values', () => {
    const initialData: ColumnJSON = {
      name: 'id',
      label: 'ID',
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
      ordering: 'ordering asc seg-1',
    };

    const column = new TableColumn(initialData, orderingArray);

    column.setLayout('center');
    expect(column.layout).toBe('center');

    column.setMaxWidth(200);
    expect(column.maxWidth).toBe(200);
  });
  test('renderDecoratorBool should return the expected string', () => {
    const initialData: ColumnJSON = {
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
      ordering: 'ordering unsorted',
    };

    const column = new TableColumn(initialData, orderingArray);
    expect(column.renderDecoratorFunction(rowData, thead)).toBe('<span style="color: red;">&#10008;</span>');
    expect(column.renderDecoratorFunction(rowData, !thead)).toBe('<span style="color: green;">&#10004;</span>');
  });
  test('renderDecoratorEmail should return the expected string', () => {
    const initialData: ColumnJSON = {
      name: 'email_field',
      label: 'Email field',
      table_classes: '',
      ordering: 'ordering unsorted',
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
    };

    const column = new TableColumn(initialData, orderingArray);
    const result = column.renderDecoratorFunction(rowData, thead);

    expect(result).toBe('<a href="mailto:test@example.com">test@example.com</a>');
    expect(column.renderDecoratorFunction({ ...rowData, email_field: 'Test Person <test@example.com>' }, thead))
      .toBe('<a href="mailto:Test Person <test@example.com>">Test Person</a>');
    expect(column.renderDecoratorFunction(rowData, !thead)).toBe(rowData.email_field);
  });
  test('renderDecoratorUrl should return the expected string', () => {
    const initialData: ColumnJSON = {
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
    };

    const column = new TableColumn(initialData, orderingArray);
    const result = column.renderDecoratorFunction(rowData, thead);

    expect(result).toBe('<a href="https://www.example.com">https://www.example.com</a>');
    expect(column.renderDecoratorFunction(rowData, !thead)).toBe(rowData.url_field);
  });
  test('renderDecoratorIpaddress should return the expected string', () => {
    const initialData: ColumnJSON = {
      name: 'ipaddress_field',
      label: 'Ipaddress field',
      table_classes: '',
      ordering: 'ordering unsorted',
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
    };

    const column = new TableColumn(initialData, orderingArray);
    const result = column.renderDecoratorFunction(rowData, thead);

    expect(result).toBe(
      '<code><span>192</span>.<span>168</span>.<span style="opacity: .5">00</span>' +
      '<span>0</span>.<span style="opacity: .5">00</span><span>1</span></code>',
    );
    expect(column.renderDecoratorFunction(rowData, !thead)).toBe(rowData.ipaddress_field);
  });
  test('renderDecoratorFile should return the expected string', () => {
    const initialData: ColumnJSON = {
      name: 'file_field',
      label: 'File field',
      table_classes: '',
      ordering: 'ordering unsorted',
      alignment: 'left',
      visibility: {
        table: 10,
        form: 10,
      },
      render_params: {
        form_component_name: 'DFile',
        input_type: 'file',
        table: 'df-tablecell-file',
        field_class: 'form-control',
      },
    };

    const column = new TableColumn(initialData, orderingArray);
    const result = column.renderDecoratorFunction(rowData, thead);

    expect(result).toBe(
      '<a href="#" onclick=\'event.stopPropagation(); window.open("example.txt", "_blank")\'>example.txt</a>',
    );

    const result2 = column.renderDecoratorFunction({ ...rowData, file_field: null }, thead);
    expect(result2).toBe(null);
    expect(column.renderDecoratorFunction(rowData, !thead)).toBe(rowData.file_field);
  });
  test('renderDecoratorCustom should return the expected string', () => {
    const initialData: ColumnJSON = {
      name: 'custom_field',
      label: 'Custom field',
      table_classes: '',
      ordering: 'ordering unsorted',
      alignment: 'left',
      visibility: {
        table: 10,
        form: 10,
      },
      render_params: {
        form_component_name: 'DInput',
        input_type: 'text',
        table: 'my_lib.decorator',
        field_class: 'form-control',
      },
    };
    window.my_lib = {};
    window.my_lib.decorator = (rec: Record<string, any>, h: boolean) => (!h ? rec.custom_field + 14 : rec.custom_field);
    const column = new TableColumn(initialData, orderingArray);
    const result = column.renderDecoratorFunction(rowData, thead);

    expect(result).toBe(42);
    expect(column.renderDecoratorFunction(rowData, !thead)).toBe(rowData.custom_field);
  });
  test('renderComponentName should return the expected value for custom component renderer', () => {
    const initialData: ColumnJSON = {
      name: 'float_field',
      label: 'Float field',
      table_classes: '',
      ordering: '',
      alignment: 'decimal',
      visibility: {
        table: 10,
        form: 10,
      },
      render_params: {
        form_component_name: 'DInput',
        input_type: 'number',
        table: '#TableCellFloat',
        table_show_zeroes: true,
        field_class: 'form-control',
      },
    };

    const column = new TableColumn(initialData, orderingArray);

    expect(column.renderComponentName).toBe('TableCellFloat');
    expect(column.align).toBe('right');
    expect(column.CSSClassHead).toBe('');
  });
});
