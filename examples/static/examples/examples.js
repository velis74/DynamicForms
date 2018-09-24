// noinspection JSUnusedGlobalSymbols
examples = {
  Fields: {note: '', unit: '', int_fld: '', qty_fld: '', cst_fld: ''},

  action_hiddenfields_note: function action_note(formID, newRec, oldRec, changedFields) {
    var fields = dynamicforms.getFieldIDs(formID);  // fields: examples.Fields
    if (changedFields.includes(fields.note)) {
      dynamicforms.fieldSetVisible(fields.unit, newRec.note != 'abc');
    }
  },

  action_hiddenfields_unit: function action_hiddenfields_unit(formID, newRec, oldRec, changedFields) {
    var fields = dynamicforms.getFieldIDs(formID);  // fields: examples.Fields
    if (changedFields.includes(fields.unit)) {
      var unit_visible = dynamicforms.fieldIsVisible(fields.unit);

      //dynamicforms.fieldSetValue(amountID, 6);
      dynamicforms.fieldSetVisible(fields.int_fld, unit_visible && ['pcs', 'cst'].includes(newRec.unit));
      dynamicforms.fieldSetVisible(fields.qty_fld, unit_visible && newRec.unit == 'wt');
      dynamicforms.fieldSetVisible(fields.cst_fld, unit_visible && newRec.unit == 'cst');
    }
  }
};
