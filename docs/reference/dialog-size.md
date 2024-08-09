# DialogSize

`DialogSize` is an enumeration that defines different sizes for dialogs.

```ts
import { DialogSize } from '@velis/dynamicforms';

enum DialogSize {
  SMALL = 1,
  MEDIUM = 2,
  LARGE = 3,
  X_LARGE = 4,
  DEFAULT = 0,
}
```

## Constants

- `defaultDialogSize`: Set to `DialogSize.DEFAULT`

## Methods

#### `fromString(size?: string): DialogSize`

Converts a string representation of size to the corresponding `DialogSize` enum value.

- Input: Optional string representing the size
- Output: Corresponding `DialogSize` enum value

Size string mappings:
- Large: "large", "lg", "modal-lg"
- Medium: "medium", "md", "modal-md"
- Small: "small", "sm", "modal-sm"
- X-Large: "x-large", "xl", "modal-xl"

If the input is undefined or doesn't match any known size, it returns `defaultDialogSize`.

#### `isDefined(size: number | string): boolean`

Checks if the given size is a valid `DialogSize` value.

- Input: A number or string representing the size
- Output: Boolean indicating whether the size is valid

::: tip
any string will evaluate to `true` since the default size is provided in case of unknown size strings.
:::

## Usage

```typescript
import { DialogSize } from '@velis/dynamicforms';

const size = DialogSize.fromString('lg');
console.log(size === DialogSize.LARGE); // true

const isValid = DialogSize.isDefined(2);
console.log(isValid); // true
```
