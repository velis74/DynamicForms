import { vi } from 'vitest';

import { gettext, interpolate } from './translations-mixin';

declare global {
  interface Window {
    gettext?: (str: string) => string;
    interpolate?: (str: string, data: any[] | { [key: string]: any }, named: boolean) => string;
  }
}

describe('Translations', () => {
  it('gettext returns string as is if window.gettext is not defined', () => {
    const str = 'Hello, World!';
    expect(gettext(str)).toBe(str);
  });

  it('gettext calls window.gettext if it is defined', () => {
    const str = 'Hello, World!';
    const translatedStr = 'Hola, Mundo!';
    global.gettext = vi.fn(() => translatedStr);

    expect(gettext(str)).toBe(translatedStr);
    expect(global.gettext).toHaveBeenCalledWith(str);

    // Clean up after the test
    delete global.gettext;
  });

  it('interpolate returns interpolated string if window.interpolate is not defined', () => {
    const str = 'Hello, %(name)s!';
    const data = { name: 'John' };
    expect(interpolate(str, data)).toBe('Hello, John!');
  });

  it('interpolate calls window.interpolate if it is defined', () => {
    const str = 'Hello, %(name)s!';
    const data = { name: 'John' };
    const interpolatedStr = 'Hola, John!';
    global.interpolate = vi.fn(() => interpolatedStr);

    expect(interpolate(str, data)).toBe(interpolatedStr);
    expect(global.interpolate).toHaveBeenCalledWith(str, data, true);

    // Clean up after the test
    delete global.interpolate;
  });
});
