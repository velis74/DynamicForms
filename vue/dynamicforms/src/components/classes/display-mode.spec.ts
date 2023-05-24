import DisplayMode, { defaultDisplayMode } from './display-mode';

describe('Display Mode', () => {
  it('Create Display Mode From String', () => {
    expect(DisplayMode.fromString('SUPPRESS')).toBe(DisplayMode.SUPPRESS);
    expect(DisplayMode.fromString('HIDDEN')).toBe(DisplayMode.HIDDEN);
    expect(DisplayMode.fromString('INVISIBLE')).toBe(DisplayMode.INVISIBLE);
    expect(DisplayMode.fromString('FULL')).toBe(DisplayMode.FULL);

    expect(DisplayMode.fromString('THIS WILL NEVER BE AN OPERATOR')).toBe(defaultDisplayMode);
  });

  it('Create Operators From Any', () => {
    expect(DisplayMode.fromAny(DisplayMode.SUPPRESS)).toBe(DisplayMode.SUPPRESS);
    expect(DisplayMode.fromAny('SUPPRESS')).toBe(DisplayMode.SUPPRESS);
    expect(DisplayMode.fromAny('SUPPRESS')).toBe(DisplayMode.fromAny(DisplayMode.SUPPRESS));

    expect(DisplayMode.fromAny(DisplayMode.HIDDEN)).toBe(DisplayMode.HIDDEN);
    expect(DisplayMode.fromAny('HIDDEN')).toBe(DisplayMode.HIDDEN);
    expect(DisplayMode.fromAny('HIDDEN')).toBe(DisplayMode.fromAny(DisplayMode.HIDDEN));

    expect(DisplayMode.fromAny(DisplayMode.INVISIBLE)).toBe(DisplayMode.INVISIBLE);
    expect(DisplayMode.fromAny('INVISIBLE')).toBe(DisplayMode.INVISIBLE);
    expect(DisplayMode.fromAny('INVISIBLE')).toBe(DisplayMode.fromAny(DisplayMode.INVISIBLE));

    expect(DisplayMode.fromAny(DisplayMode.FULL)).toBe(DisplayMode.FULL);
    expect(DisplayMode.fromAny('FULL')).toBe(DisplayMode.FULL);
    expect(DisplayMode.fromAny('FULL')).toBe(DisplayMode.fromAny(DisplayMode.FULL));

    expect(DisplayMode.fromAny(100)).toBe(defaultDisplayMode);
    expect(DisplayMode.fromAny('THIS WILL NEVER BE AN OPERATOR')).toBe(defaultDisplayMode);
  });
  it('Check If Defined', () => {
    expect(DisplayMode.isDefined(100)).toBe(false);
    expect(DisplayMode.isDefined('SUPPRESS')).toBe(true);
    expect(DisplayMode.isDefined('HIDDEN')).toBe(true);
    expect(DisplayMode.isDefined('INVISIBLE')).toBe(true);
    expect(DisplayMode.isDefined('FULL')).toBe(true);
    expect(DisplayMode.isDefined('THIS WILL NEVER BE AN OPERATOR')).toBe(true);
  });
});
