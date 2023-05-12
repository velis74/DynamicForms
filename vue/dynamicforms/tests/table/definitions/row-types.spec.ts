import RowTypes from '../../../src/components/table/definitions/row-types';

describe('Row Types', () => {
  it('Check Is defined', () => {
    expect(RowTypes.isDefined(100)).toBe(false);
    expect(RowTypes.isDefined(RowTypes.Label)).toBe(true);
    expect(RowTypes.isDefined(RowTypes.Filter)).toBe(true);
    expect(RowTypes.isDefined(RowTypes.Data)).toBe(true);
  });
  it('Check If Row Is Table Head', () => {
    expect(RowTypes.isTHead(RowTypes.Label)).toBe(true);
    expect(RowTypes.isTHead(RowTypes.Filter)).toBe(true);
    expect(RowTypes.isTHead(RowTypes.Data)).toBe(false);
  });
});
