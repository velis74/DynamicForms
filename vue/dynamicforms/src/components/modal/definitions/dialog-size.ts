enum DialogSize {
  SMALL = 1,
  MEDIUM = 2,
  LARGE = 3,
  X_LARGE = 4,
  DEFAULT = 0,
}

export const defaultDialogSize: DialogSize = DialogSize.DEFAULT;

namespace DialogSize {
  const largeIdentifiers: string[] = ['large', 'lg', 'modal-lg'];
  const mediumIdentifiers: string[] = ['medium', 'md', 'modal-md'];
  const smallIdentifiers: string[] = ['small', 'sm', 'modal-sm'];
  const xLargeIdentifiers: string[] = ['x-large', 'xl', 'modal-xl'];

  export function fromString(size?: string): DialogSize {
    if (size === undefined) return defaultDialogSize;
    if (largeIdentifiers.includes(size)) return DialogSize.LARGE;
    if (mediumIdentifiers.includes(size)) return DialogSize.MEDIUM;
    if (smallIdentifiers.includes(size)) return DialogSize.SMALL;
    if (xLargeIdentifiers.includes(size)) return DialogSize.X_LARGE;
    return defaultDialogSize;
  }

  export function isDefined(size: number | string) {
    const check = (typeof size === 'number') ? size : DialogSize.fromString(size as string);
    return Object.values(DialogSize).includes(check);
  }
}

Object.freeze(DialogSize);
export default DialogSize;
