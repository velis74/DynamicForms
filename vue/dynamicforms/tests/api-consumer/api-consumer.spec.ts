import { vi } from 'vitest';

import ConsumerLogicApi from '../../src/components/api_consumer/consumer-logic-api';

import * as mockComponentDef from './api-consumer-table-componentdef.json';

vi.mock('axios', () => {
  const res = {
    get: async (url: string) => {
      if (url.includes('failure')) throw Error('Refusing to return definition');
      return { data: mockComponentDef };
    },
    create: () => res,
    interceptors: {
      request: { use: vi.fn(), eject: vi.fn() },
      response: { use: vi.fn(), eject: vi.fn() },
    },
  };
  return { default: res };
});

describe('APIConsumerLogic', () => {
  it('fails to load data from a bad url', async () => {
    const apiConsumer = new ConsumerLogicApi('failure');
    await expect(apiConsumer.getFullDefinition()).rejects.toThrowError('Refusing to return definition');
  });
  it('loads the data and composes the fields, tableColumns collections', async () => {
    const apiConsumer = new ConsumerLogicApi('/hidden-fields');
    await apiConsumer.getFullDefinition();
    const allProps = [
      'id', 'df_control_data', 'df_prev_id', 'row_css_style', 'note', 'unit', 'int_fld', 'qty_fld',
      'cst_fld', 'additional_text', '#actions-row_end',
    ];
    expect(Object.keys(apiConsumer.fields).sort()).toEqual(allProps.sort());
    expect(apiConsumer.tableColumns.map((col) => col.name).sort()).toEqual(allProps.sort());
  });
});
