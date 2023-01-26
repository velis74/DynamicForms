const DialogSize = {
  SMALL: 1,
  LARGE: 2,
  X_LARGE: 3,
  DEFAULT: 0,

  fromString(size: string) {
    if (['large', 'lg', 'modal-lg'].includes(size)) return DialogSize.LARGE;
    if (['small', 'sm', 'modal-sm'].includes(size)) return DialogSize.SMALL;
    if (['x-large', 'xl', 'modal-xl'].includes(size)) return DialogSize.X_LARGE;
    return DialogSize.DEFAULT;
  },

  isDefined(size: number | string) {
    const check = (typeof size === 'number') ? size : DialogSize.fromString(size as string);
    return check >= 0 && check <= 3;
  },
} as const;

export default Object.freeze(DialogSize);
