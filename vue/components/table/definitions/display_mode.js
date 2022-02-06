import Enum from 'enum';

export default new Enum({
  // This enum is actually declared in dynamicforms.mixins.field_render.py
  SUPPRESS: 1, // Field will be entirely suppressed. it will not render (not even to JSON) and will not parse for PUT
  HIDDEN: 5, // Field will render as <input type="hidden"> or <tr data-field_name>
  INVISIBLE: 8, // Field will render completely, but with display: none. Equal to setting its style = {display: none}
  FULL: 10, // Field will render completely
}, { freeze: true });
