enum DialogSize {
  SMALL = 1,
  MEDIUM = 2,
  LARGE = 3,
  X_LARGE = 4,
  DEFAULT = 0,
}

namespace DialogSize {
  export function fromString(size: string) {
    if (['large', 'lg', 'modal-lg'].includes(size)) return DialogSize.LARGE;
    if (['medium', 'md', 'modal-md'].includes(size)) return DialogSize.MEDIUM;
    if (['small', 'sm', 'modal-sm'].includes(size)) return DialogSize.SMALL;
    if (['x-large', 'xl', 'modal-xl'].includes(size)) return DialogSize.X_LARGE;
    return DialogSize.DEFAULT;
  }

  export function isDefined(size: number | string) {
    const check = (typeof size === 'number') ? size : DialogSize.fromString(size as string);
    return Object.values(DialogSize).includes(check);
  }
}

Object.freeze(DialogSize);

export default DialogSize;
