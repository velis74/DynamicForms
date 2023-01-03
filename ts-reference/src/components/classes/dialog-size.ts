enum DialogSize {
  SMALL = 1,
  LARGE = 2,
  X_LARGE = 3,
  DEFAULT = 0,
  isDefined,
}

export function fromString(size: string) {
  if (['large', 'lg', 'modal-lg'].includes(size)) return DialogSize.LARGE;
  if (['small', 'sm', 'modal-sm'].includes(size)) return DialogSize.SMALL;
  if (['x-large', 'xl', 'modal-xl'].includes(size)) return DialogSize.X_LARGE;
  return DialogSize.DEFAULT;
}

export function isDefined(value: number) {
  return value in DialogSize;
}

export default DialogSize;
