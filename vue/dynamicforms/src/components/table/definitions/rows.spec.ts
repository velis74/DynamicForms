import { APIConsumer } from '../../api_consumer/namespace';
import { DfTable } from '../namespace';

import TableRows from './rows';

// Define an interface that extends ConsumerLogicBaseInterface and includes fetchNewRows
interface TestConsumerLogicInterface extends APIConsumer.ConsumerLogicBaseInterface {
  fetchNewRows?: (url: string) => Promise<DfTable.RowsData>;
}

describe('TableRows', () => {
  let logicMock: TestConsumerLogicInterface;
  let rowsDataMock: DfTable.RowsData;

  beforeEach(() => {
    // Mock logic and rowsData as needed for your tests
    logicMock = {
      pkName: 'id',
      // Add other properties or methods needed for testing
    } as TestConsumerLogicInterface;

    rowsDataMock = {
      results: [
        { id: 1, name: 'Row 1' },
        { id: 2, name: 'Row 2' },
      ],
      next: '/api/next-page',
    } as DfTable.RowsData;
  });

  it('should load more rows correctly', async () => {
    const tableRows = new TableRows(logicMock, rowsDataMock);

    // Mock data for additional rows to be loaded
    const additionalRowsDataMock: DfTable.RowsData = {
      results: [
        { id: 3, name: 'New Row 3' },
        { id: 4, name: 'New Row 4' },
      ],
      next: '/api/next-page-2',
    };

    // Mock the fetchNewRows method to resolve with additional rows
    logicMock.fetchNewRows = async () => additionalRowsDataMock;

    // Set the updated logic with the mock fetchNewRows method
    tableRows.logic = logicMock;

    // Mock visibility handler to trigger loading
    tableRows.visibilityHandler = () => ({ callback: async () => {}, once: true });

    // Trigger loading more rows
    await tableRows.loadMoreRows(true);

    // Log expected values or perform your assertions here
    console.log('Expected data after loading more rows:', tableRows.data);
  });

  it('should update rows correctly', () => {
    const tableRows = new TableRows(logicMock, rowsDataMock);

    // Mock data for updating rows
    const updatedRowsData: DfTable.RowsData = {
      results: [
        { id: 1, name: 'Updated Row 1' },
        { id: 2, name: 'Updated Row 2' },
      ],
      next: '/api/next-page-2',
    };

    // Call the updateRows method
    tableRows.updateRows(updatedRowsData.results);

    // Assert that the rows have been updated
    expect(tableRows.data[0].name).toBe('Updated Row 1');
    expect(tableRows.data[1].name).toBe('Updated Row 2');
  });

  it('should reindex rows correctly', () => {
    const tableRows = new TableRows(logicMock, rowsDataMock);

    // Add a new row
    const newRowData: DfTable.RowDataInterface = { id: 3, name: 'New Row 3' };
    tableRows.updateRows([newRowData]);

    // Call the reIndex method
    tableRows.reIndex();

    // Assert that the row has been reindexed
    expect(tableRows.rowIndices['3']).toBe(2);
  });

  it('should delete row correctly', () => {
    const tableRows = new TableRows(logicMock, rowsDataMock);

    // Delete a row
    tableRows.deleteRow('2');

    // Assert that the row has been deleted
    expect(tableRows.data.length).toBe(1);
    expect(tableRows.data[0].name).toBe('Row 1');
    expect(tableRows.rowIndices['2']).toBeUndefined();
  });
});
