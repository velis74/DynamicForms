import DialogSize from '../../components/classes/dialog_size';

// eslint-disable-next-line no-undef
describe('DialogSize', () => {
  // eslint-disable-next-line no-undef
  it('Check if string matches enum', () => {
    const t = () => {
      DialogSize.x = 2;
    };
    // eslint-disable-next-line no-undef
    expect(DialogSize.fromString('sm')).toEqual(DialogSize.SMALL);
    // eslint-disable-next-line no-undef
    expect(DialogSize.fromString('large')).toEqual(DialogSize.LARGE);
    // eslint-disable-next-line no-undef
    expect(DialogSize.fromString('modal-xl')).toEqual(DialogSize.X_LARGE);
    // eslint-disable-next-line no-undef
    expect(DialogSize.fromString('')).toEqual(DialogSize.DEFAULT);
    // eslint-disable-next-line no-undef
    expect(t).toThrow(TypeError);
  });
});
