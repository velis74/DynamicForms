enum ComponentDisplay {
  // This enum is actually declared in dynamicforms.mixins.field_render.py
  TABLE = 1,
  FORM = 2,
  DIALOG = 3,
}

namespace ComponentDisplay {
  export function fromString(display: string) {
    if (display.toUpperCase() === 'TABLE') return ComponentDisplay.TABLE;
    if (display.toUpperCase() === 'FORM') return ComponentDisplay.FORM;
    if (display.toUpperCase() === 'DIALOG') return ComponentDisplay.DIALOG;
    return ComponentDisplay.TABLE;
  }

  export function isDefined(display: number | string) {
    const check = (typeof display === 'number') ? display : ComponentDisplay.fromString(display as string);
    return Object.values(ComponentDisplay).includes(check);
  }
}

Object.freeze(ComponentDisplay);

export default ComponentDisplay;
