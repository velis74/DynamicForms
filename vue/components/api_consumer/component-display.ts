import Enum from 'enum';

export default new Enum({
  // This enum is actually declared in dynamicforms.mixins.field_render.py
  TABLE: 1,
  FORM: 2,
  DIALOG: 3,
}, { freeze: true });
