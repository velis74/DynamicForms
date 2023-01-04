import DialogSize from '../../components/modal/dialog-size';

describe('DialogSize', () => {
  // eslint-disable-next-line no-undef
  it('Check if string matches enum', () => {
    const t = () => {
      // @ts-ignore: we text that x does not exist and that it cannot be set. hence: TS2339
      DialogSize.x = 2;
    };
    expect(DialogSize.fromString('sm')).toEqual(DialogSize.SMALL);
    expect(DialogSize.fromString('large')).toEqual(DialogSize.LARGE);
    expect(DialogSize.fromString('modal-xl')).toEqual(DialogSize.X_LARGE);
    expect(DialogSize.fromString('')).toEqual(DialogSize.DEFAULT);
    expect(t).toThrow(TypeError);
  });
});
