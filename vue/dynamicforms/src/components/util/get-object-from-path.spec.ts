import getObjectFromPath from './get-object-from-path';

describe('getObjectFromPath', () => {
  beforeEach(() => {
    // Mocking the global window object
    // Note: Only adding properties needed for the test
    (global as any).window = {
      property1: { nestedProperty: 'nested value' },
      property2: 'value2',
    };
  });

  afterEach(() => {
    // Reset the global window object after each test
    delete (global as any).window;
  });

  it('returns the correct value when path is valid', () => {
    expect(getObjectFromPath('property1.nestedProperty')).toBe('nested value');
    expect(getObjectFromPath('property2')).toBe('value2');
  });

  it('returns an empty object when path does not exist', () => {
    const result = getObjectFromPath('property3');
    expect(result).toEqual({});
    expect(Object.keys(result).length).toBe(0);
  });

  it('returns undefined when path is not provided', () => {
    expect(getObjectFromPath('')).toBeUndefined();
    expect(getObjectFromPath(null as any)).toBeUndefined();
  });
});
